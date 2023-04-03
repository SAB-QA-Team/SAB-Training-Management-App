from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.admin.username

class Manager(models.Model):
    manager = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)

    def __str__(self):
            return self.manager.first_name + ' ' + self.manager.last_name
    
class Trainee(models.Model):
    trainee = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)
    organization = models.CharField(max_length=200)
    job = models.CharField(max_length=100)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return self.trainee.get_name()


class Instructor(models.Model):
     id = models.AutoField(primary_key=True)
     first_name = models.CharField(max_length=255)
     last_name = models.CharField(max_length=255)
     email = models.EmailField(max_length=156)
     phone = models.CharField(max_length= 20)

     def __str__(self):
          return self.first_name + " " + self.last_name
     
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    number_of_classes = models.PositiveIntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    current_session = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classes_attended = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.trainee} registered for {self.course.name}"
    
class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    session_number = models.IntegerField()
    time_entered = models.DateTimeField(auto_now_add=True)
    time_existed = models.DateTimeField(null=True)
    attended = models.BooleanField(default=False)


