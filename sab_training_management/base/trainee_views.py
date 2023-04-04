#This file is not complete, its the blueprint for courses listing
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test

from datetime import datetime, date
from .models import *
from django.urls import reverse_lazy
#To deal with login and signup
from django.http import Http404
from django.http import HttpResponse

from accounts.views import *
from .forms import TraineeRegistrationForm

from .views import *

#Certififacte Generation
import io
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import FileResponse

#Registration
def register_trainee(request):
    if request.method == 'POST':
        form = TraineeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            trainee = Trainee(trainee=user)
            trainee.phone = form.cleaned_data['phone']
            trainee.address = form.cleaned_data['address']
            trainee.organization = form.cleaned_data['organization']
            trainee.job = form.cleaned_data['job']
            #Fix this for multiple managers
            trainee.manager = Manager.objects.filter(organization=trainee.organization).first()
            trainee.save()
            return redirect('login')
        else:
            print("Form errors:", form.errors)  # Print the form errors
    else:
        form = TraineeRegistrationForm()
    return render(request, 'base/register.html', {'form': form})

def contact(request):
    return render(request, 'base/contact.html')

@user_passes_test(is_trainee, login_url='login')
def profile(request):
    trainee = Trainee.objects.get(trainee=request.user)
    context = {'trainee':trainee}
    return render(request, 'base/profile.html', context)

@user_passes_test(is_trainee, login_url='login')
#Courses lisintg management
def courses_list(request):
    print(request.user)
    trainee = Trainee.objects.get(trainee = request.user)
    traineeCourses = Attendance.objects.filter(trainee = trainee)

    courses = []
    for traineeCourse in traineeCourses:
        courses += [traineeCourse.course]

    otherCourses = []
    allCourses = Course.objects.all()
    for course in allCourses:
        if course not in courses:
            otherCourses += [course]

    context = {
        'courses': otherCourses
    }
    return render(request, "base/courses_list.html", context)

#Add lambda
@user_passes_test(lambda u: u.is_trainee or u.is_manager, login_url='login')
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {'course':course}
    return render(request,'base/course_details.html',context)  

@user_passes_test(is_trainee, login_url='login')
def trainee_courses(request):
    # need to generalize so that it takes in the logged in trainee
    trainee = Trainee.objects.get(trainee=request.user)
    traineeCourses = Attendance.objects.filter(trainee = trainee)
    current_date = date.today()
    ongoing = []
    completed = []
    incomplete = []
    for traineeCourse in traineeCourses:
        if current_date < traineeCourse.course.end_date:
            ongoing += [traineeCourse]
        else:
            if traineeCourse.classes_attended / traineeCourse.course.number_of_classes > 0.9:
                completed += [traineeCourse]
            else:
                incomplete += [traineeCourse]

    context = {
        'ongoing': ongoing, 'completed': completed, 'incomplete':incomplete
    }
    return render(request, "base/my_courses.html", context)


@user_passes_test(is_trainee, login_url='login')
def register_course(request, course_id):
    # get the list of courses the trainee is already registered for
    traineeObj = Trainee.objects.get(trainee=request.user)
    courseObj = Course.objects.get(id=course_id)
    # only register if there is enough space
    if courseObj.capacity > 0:
        new_record = Attendance(trainee=traineeObj, course=courseObj, classes_attended=0)
        new_record.save()
        courseObj.capacity -= 1
        courseObj.save()
    
    return redirect("my-courses")


################################################

def enter_class(request, course_id):
    traineeObj = Trainee.objects.get(trainee=request.user)
    courseObj = Course.objects.get(id=course_id)
    currSession = courseObj.current_session

    # only if this trainee did not attend this session in this course yet, create a new record
    if Session.objects.filter(course=courseObj, trainee=traineeObj, session_number=currSession).exists() == False:
        newSession = Session(course=courseObj, trainee=traineeObj, session_number=currSession)
        newSession.save()

    return redirect('my-courses')


def exist_class(request, course_id):
    traineeObj = Trainee.objects.get(trainee=request.user)
    courseObj = Course.objects.get(id=course_id)
    currSession = courseObj.current_session

    # you can only exist a class session if you entered it first
    if Session.objects.filter(course=courseObj, trainee=traineeObj, session_number=currSession).exists():
        currSession = Session.objects.get(course=courseObj, trainee=traineeObj, session_number=currSession)
        # if the trainee has not attended this session yet
        if currSession.attended == False:
            current_time = datetime.now() 
            currSession.time_existed = current_time
            currSession.attended = True
            currSession.save()

            # increment attendance record for this trainee in this course
            attendace_record = Attendance.objects.get(trainee=traineeObj, course=courseObj)
            attendace_record.classes_attended += 1
            attendace_record.save()
    
    return redirect('my-courses')



def drop_course(request, course_id):
    currCourse = Course.objects.get(id=course_id)
    currTrainee = Trainee.objects.get(trainee=request.user)
    attendance_instance = Attendance.objects.get(course=currCourse, trainee=currTrainee)
    currCourse.capacity += 1
    currCourse.save()
    attendance_instance.delete()
    return redirect('my-courses')

def generate_certificate(request, course_id):
    # Get the user's name
    user_name = request.user.get_name()
    currCourse = Course.objects.get(id=course_id)
    # Load the certificate template PDF
    template_path = 'base/static/certificate_template.pdf'
    template = PyPDF2.PdfReader(template_path)

    # Create a new PDF with the user's name
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

    # Add user's name at the appropriate coordinates (customize as needed)
    c.saveState()  # Save the current state of the canvas
    c.rotate(-90)  # Set the rotation angle to -90 degrees to counter the template rotation
    c.setFont("Helvetica", 24)
    c.drawString(-440, 290, user_name)  # Update coordinates accordingly
    c.restoreState()  # Restore the previous state of the canvas
 
    # Add course name
    c.saveState()  # Save the current state of the canvas
    c.rotate(-90)  # Set the rotation angle to -90 degrees to counter the template rotation
    c.setFont("Helvetica", 24)
    c.drawString(-440, 360, currCourse.name)  # Update coordinates accordingly
    c.restoreState()  # Restore the previous state of the canvas

    # Add course dates
    c.saveState()  # Save the current state of the canvas
    c.rotate(-90)  # Set the rotation angle to -90 degrees to counter the template rotation
    c.setFont("Helvetica", 16)
    c.drawString(-360, 400, str(currCourse.start_date))  # Update coordinates accordingly
    c.restoreState()  # Restore the previous state of the canvas

    c.saveState()  # Save the current state of the canvas
    c.rotate(-90)  # Set the rotation angle to -90 degrees to counter the template rotation
    c.setFont("Helvetica", 16)
    c.drawString(-490, 400, str(currCourse.end_date))  # Update coordinates accordingly
    c.restoreState()  # Restore the previous state of the canvas

    # Combine the new PDF with the certificate template
    c.save()
    buffer.seek(0)
    new_pdf = PyPDF2.PdfReader(buffer)

    output = io.BytesIO()
    pdf_writer = PyPDF2.PdfWriter()

    # Merge the two PDFs
    page = template.pages[0]
    page.merge_page(new_pdf.pages[0])
    pdf_writer.add_page(page)

    # Save the final PDF
    pdf_writer.write(output)
    output.seek(0)

    # Return the PDF as a response
    response = FileResponse(output, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=certificate_{user_name}.pdf'

    return response

