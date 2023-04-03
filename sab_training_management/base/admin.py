from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Admin)
admin.site.register(Trainee)
admin.site.register(Manager)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Instructor)
admin.site.register(Session)