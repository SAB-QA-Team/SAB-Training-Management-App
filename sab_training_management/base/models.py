from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
    #Admin_id = int
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Trainee(models.Model):
    qid = models.CharField(max_length=11)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.firstName + ' ' + self.lastName

class Manager(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)

    def __str__(self):
            return self.firstName + ' ' + self.lastName
