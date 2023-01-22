from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .manager import FirstManager


#Making custom User model

class MyRegistration(AbstractBaseUser, PermissionsMixin):
    location_list=[
        ('Solapur', 'Solapur'),
        ('Dhule', 'Dhule'),
        ('Other', 'Other'),
        ]
    username=models.CharField(max_length=10, unique=True)
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    location=models.CharField(max_length=10, choices=location_list, default=None)
    designation=models.CharField(max_length=70)
    is_active=models.BooleanField()
    is_staff=models.BooleanField(default=False)
    start_date=models.DateTimeField(default=timezone.now)
    last_login=models.DateTimeField(null=True)


    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['email', 'first_name', 'last_name', 'location', 'designation']
    objects=FirstManager()
    def __str__(self):
        return self.first_name