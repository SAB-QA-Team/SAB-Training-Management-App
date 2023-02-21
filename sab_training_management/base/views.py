#This file is not complete, its the blueprint for courses listing
from django.shortcuts import render
from .models import Trainee
#from django.views.generic.list import ListView

from django.urls import reverse_lazy
#To deal with login and signup
from django.contrib.auth.views import LoginView
from django.http import HttpResponse

def login(request):
    return HttpResponse('MAIN PAGE')

def form1(request):
    model = Trainee
    return HttpResponse(request)
#from .model import Course #When database is implemented

#Login
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('courses')

#Registration
class CustomRegistrationView(LoginView):
    model = Trainee
    template_name = 'base/register.html'
    fields = '__all__'
    redirect_authenticated_user = True

#    def get_success_url(self):
#        return reverse_lazy('courses')
    

#Courses lisintg management
#class CourseList(ListView):
#    model = Course
#    context_object_name = 'courses'
