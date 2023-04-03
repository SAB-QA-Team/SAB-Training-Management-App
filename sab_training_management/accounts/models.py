from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ROLE_CHOICES = (
        ('trainee', 'Trainee'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="trainee")
    
    #2fa
    secret_key = models.CharField(max_length=16, blank=True, null=True)
    #is_staff and is_active ?
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = "email", "first_name", "last_name", "role"

    def is_admin(self):
        return self.role == "admin"
    
    def is_manager(self):
        return self.role == "manager"
    
    def is_trainee(self):
        return self.role == "trainee"
    
    def set_username(self, username):
        self.username = username

    def set_email(self, email):
        self.email = email
    
    def set_first_name(self, first_name):
        self.first_name = first_name
    
    def set_last_name(self, last_name):
        self.last_name = last_name
        
    def get_name(self):
        return self.first_name + " " + self.last_name
    
    def get_email(self):
        return self.email
    
    def __str__(self):
        return self.username