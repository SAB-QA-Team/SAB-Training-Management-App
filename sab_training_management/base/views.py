#This file is not complete, its the blueprint for courses listing
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import *
from django.urls import reverse_lazy
#To deal with login and signup
from django.http import Http404
from django.http import HttpResponse

from accounts.views import *
from .forms import ManagerRegistrationForm, ManagerEditForm, TraineeEditForm

#2FA Libs
from django.contrib.auth.decorators import login_required
from accounts.utils import generate_secret_key
import pyotp
from django.contrib import messages
from .forms import AuthenticationTokenForm

#Login

#Temporary (needs user specific accesses)
def login_view(request):
    if request.method == 'POST':
        #Retrieve data from the POST request for authentication
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            #Manage first login
            if user.secret_key is None:
                #if request.user.is_admin():
                #    return redirect("trainees")
                #elif request.user.is_trainee():
                #    return redirect("courses-list")
                #elif request.user.is_manager():
                #    return redirect("manager-dashboard")
                return redirect('two-factor-auth-setup')
            if user.secret_key and not request.session.get('two_factor_authenticated', False):
                return redirect("two-factor-auth")
            return redirect("login")
        else:
            error_message = "Invalid Credentials"
    else:
        error_message = None
    return render(request, "base/login.html", {'error_message': error_message})

#2FA Views

@login_required
def qr_code(request):
    if not request.user.secret_key:
        secret_key = generate_secret_key()
        request.user.secret_key = secret_key
        request.user.save()
    otp_uri = pyotp.totp.TOTP(request.user.secret_key).provisioning_uri(name=request.user.username, issuer_name='My App')
    return render(request, 'base/qr_code.html', {'otp_uri': otp_uri})

@login_required
def two_factor_auth_setup(request):
    return render(request, 'base/2fa_setup.html')

@login_required
def two_factor_auth(request):
    if request.method == 'POST':
        form = AuthenticationTokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            if pyotp.totp.TOTP(request.user.secret_key).verify(token):
                request.session['two_factor_authenticated'] = True
                messages.success(request, 'You have been successfully authenticated.')
                #return redirect('home')
                #Redirect user to appropriate page
                if request.user.is_admin():
                    return redirect("trainees")
                elif request.user.is_trainee():
                    return redirect("courses-list")
                elif request.user.is_manager():
                    return redirect("manager-trainees")
            else:
                messages.error(request, 'Invalid authentication code. Please try again.')
    else:
        form = AuthenticationTokenForm()
    return render(request, 'base/two_factor_auth.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

#To ensure that users access their pages
def is_admin(user):
    return user.is_authenticated and user.is_admin()

def is_trainee(user):
    return user.is_authenticated and user.is_trainee()

def is_manager(user):
    return user.is_authenticated and user.is_manager()

#Admin
@user_passes_test(is_admin, login_url='login')
def dashboard(request):
    return render(request,'base/dashboard.html')  

# Create your views here.
class InstructorList(ListView):
    model = Instructor
    template_name = 'base/admin_dashboard/instructor_list.html'
    context_object_name = 'instructors'

class InstructorDetail(DetailView):
    model = Instructor
    template_name = 'base/admin_dashboard/instructor_detail.html'
    context_object_name = 'instructor'

class InstructorCreate(CreateView):
    model = Instructor
    template_name = 'base/admin_dashboard/instructor_form.html'
    fields = '__all__'
    success_url = reverse_lazy("instructors")

class InstructorUpdate(UpdateView):
    model = Instructor
    template_name = 'base/admin_dashboard/instructor_form.html'
    fields = '__all__'
    success_url = reverse_lazy("instructors")

class InstructorDelete(DeleteView):
    model = Instructor
    template_name = 'base/admin_dashboard/instructor_confirm_delete.html'
    context_object_name = 'instructor'
    success_url = reverse_lazy("instructors")


class CourseList(ListView):
    model = Course
    template_name = 'base/admin_dashboard/course_list.html'
    context_object_name = 'courses'

class CourseDetail(DetailView):
    model = Course
    template_name = 'base/admin_dashboard/course_detail.html'
    context_object_name = 'course'

class CourseCreate(CreateView):
    model = Course
    template_name = 'base/admin_dashboard/course_form.html'
    fields = '__all__'
    success_url = reverse_lazy("courses")

class CourseUpdate(UpdateView):
    model = Course
    template_name = 'base/admin_dashboard/course_form.html'
    fields = '__all__'
    success_url = reverse_lazy("courses")

class CourseDelete(DeleteView):
    model = Course
    template_name = 'base/admin_dashboard/course_confirm_delete.html'
    context_object_name = 'course'
    success_url = reverse_lazy("courses")

def increment_session(request, course_id):
    courseObj = Course.objects.get(id=course_id)
    courseObj.current_session += 1
    courseObj.save()
    return redirect('courses')

def manager_list(request):
    managers = Manager.objects.all()
    context = {'managers': managers}
    return render(request, 'base/admin_dashboard/manager_list.html', context)


class ManagerDetail(DetailView):
    model = Manager
    template_name = 'base/admin_dashboard/manager_detail.html'
    context_object_name = 'manager'

@login_required
def create_manager(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            # Create the CustomUser instance
            user = CustomUser.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=form.cleaned_data['password1']
            )
            # Create the Manager instance
            manager = Manager.objects.create(
                manager=user,
                phone=form.cleaned_data['phone'],
                organization=form.cleaned_data['organization']
            )
            # Redirect the user to the manager detail page
            return redirect('manager', pk=manager.id)
    else:
        form = ManagerRegistrationForm()
    return render(request, 'base/admin_dashboard/manager_create.html', {'form': form})

@login_required
def edit_manager(request, manager_id):
    manager = get_object_or_404(Manager, pk=manager_id)
    user = manager.manager
    if request.method == 'POST':
        form = ManagerEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            # Update Manager fields
            manager.phone = form.cleaned_data['phone']
            manager.organization = form.cleaned_data['organization']
            manager.save()
            return redirect('managers')
        else:
            print(form.errors)
    else:
        form = ManagerEditForm(instance=user, initial={
            'phone': manager.phone,
            'organization': manager.organization
        })
    return render(request, 'base/admin_dashboard/manager_edit.html', {'form': form})



@login_required
def delete_manager(request, pk):
    manager = get_object_or_404(Manager, pk=pk)
    user = manager.manager
    manager.delete()
    user.delete()
    
    return redirect('managers')

@login_required
def trainee_list(request):
    trainees = Trainee.objects.all()
    context = {'trainees': trainees}
    return render(request, 'base/admin_dashboard/trainee_list.html', context)

class TraineeDetail(DetailView):
    model = Trainee
    template_name = 'base/admin_dashboard/trainee_detail.html'
    context_object_name = 'trainee'

class TraineeCreate(CreateView):
    model = Trainee
    template_name = 'base/admin_dashboard/trainee_form.html'
    fields = '__all__'
    success_url = reverse_lazy('trainees')

@login_required
def edit_trainee(request, trainee_id):
    trainee = get_object_or_404(Trainee, pk=trainee_id)
    user = trainee.trainee
    if request.method == 'POST':
        form = TraineeEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            # Update Manager fields
            trainee.phone = form.cleaned_data['phone']
            trainee.job = form.cleaned_data['job']
            trainee.save()
            return redirect('trainees')
        else:
            print(form.errors)
    else:
        form = TraineeEditForm(instance=user, initial={
            'phone': trainee.phone,
            'address': trainee.address,
            'job': trainee.job
        })
    return render(request, 'base/admin_dashboard/trainee_form.html', {'form': form})



@login_required
def delete_trainee(request, pk):
    trainee = get_object_or_404(Trainee, pk=pk)
    user = trainee.trainee
    trainee.delete()
    user.delete()
    
    return redirect('trainees')

