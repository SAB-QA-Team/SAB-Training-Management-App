#This file is not complete, its the blueprint for courses listing
from django.shortcuts import render
#from django.views.generic.list import ListView

from django.urls import reverse_lazy
#To deal with login and signup
from django.contrib.auth.views import LoginView


#from .model import Course #When database is implemented

#Login
class CustomLoginView(LoginView):
    template_name = template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('courses')

#Courses lisintg management
#class CourseList(ListView):
#    model = Course
#    context_object_name = 'courses'
