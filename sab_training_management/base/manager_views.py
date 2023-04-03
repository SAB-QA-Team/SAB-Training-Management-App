from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, date
from .models import Instructor, Course, Manager, Trainee, Attendance, Session


def managerTrainees(request):
    thisManager = Manager.objects.get(manager=request.user)
    trainees = Trainee.objects.filter(manager=thisManager)
    context = {'trainees':trainees}
    return render(request, "base/manager/my_trainees.html", context)

def traineeCourses(request, trainee_id):
    thisTrainee = Trainee.objects.get(id=trainee_id)
    traineeCourses = Attendance.objects.filter(trainee=thisTrainee)
    current_date = date.today()
    context = {'traineeCourses': traineeCourses, 'trainee':thisTrainee, 'current_date': current_date}
    return render(request, "base/manager/my_trainee_courses.html", context)