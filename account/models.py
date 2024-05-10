from datetime import datetime, timedelta
import uuid
from django.db import models
# import pytz
from account.manager import UserManager
from django.contrib.auth.models import AbstractUser

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
    # username=None
    avatar = models.ImageField(upload_to='avatars/')
    email=models.EmailField(max_length=200,unique=True)
    phone=models.CharField(max_length=10,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    
    # objects = UserManager()
    
    # USERNAME_FIELD='id'
    # REQUIRED_FEILDS=[]
    def __str__(self):
        return self.email
