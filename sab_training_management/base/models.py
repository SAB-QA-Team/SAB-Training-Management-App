from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Admin(models.Model):
    Admin_id: int
    Name: models.CharField()
    Email: models.CharField()
    Phone_number: models.CharField()

    def __str__(self):
        return self.Name

#test


