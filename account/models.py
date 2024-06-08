from datetime import datetime, timedelta
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from main.models import Course

# _genders = [("m","Male"),
#            ("f","Female"),
#            ("o","Other")]

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/',null = True, blank=True)
    email=models.EmailField(max_length=200,unique=True)
    phone=models.CharField(max_length=10,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    
    def toJson(self)->dict:
        data = {
            "id":self.id,
            "avatar":self.avatar.url,
            "username":self.username,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "email":self.email,
            "phone":self.phone,
            "date_of_birth":str(self.dob),
            "address":self.address,
        }
        return data
    
    def __str__(self):
        return self.email
    
class Subscription(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True)
    class Meta:
        unique_together = ('user', 'course',)
    
class Key(models.Model):
    id = models.BigIntegerField(primary_key=True)
    otp = models.IntegerField(null=True,blank=True,unique=True)
    key = models.CharField(null=True,blank=True, max_length=40)
    expiry = models.DecimalField(null=True,blank=True,decimal_places=9,max_digits=20)
    created = models.DateTimeField(auto_now_add=True)
