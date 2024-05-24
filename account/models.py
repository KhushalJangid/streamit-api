from datetime import datetime, timedelta
import uuid
from django.db import models
# import pytz
from account.manager import UserManager
from django.contrib.auth.models import AbstractUser

from main.models import Course

_genders = [("m","Male"),
           ("f","Female"),
           ("o","Other")]

genders = {
    'Male':'m',
    'Female':'f',
    'Other':'o',
}

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/',null = True, blank=True)
    email=models.EmailField(max_length=200,unique=True)
    phone=models.CharField(max_length=10,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.email
    
class Subscription(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)
    created = models.DateTimeField(default='django.utils.timezone.now')
    expiry = models.DateTimeField(null=True)
