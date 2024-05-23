import uuid
from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=250)
    type = models.CharField(max_length=25)
    uniqueName = models.UUIDField(default=uuid.uuid4,editable=False)
    price = models.IntegerField(default=0)
    uploadDate = models.DateTimeField(default=timezone.now)
    
    def toJson(self)->dict:
        js =  {
            "id":self.id,
            "title":self.title,
            "type":self.type,
            "uniqueName":self.uniqueName,
            "price":self.price,
            "uploadDate":self.uploadDate
        }
        return js
    def __str__(self) -> str:
        return self.title
    
class VideoAsset(models.Model):
    title = models.CharField(max_length=250)
    uniqueName = models.UUIDField(default=uuid.uuid4,editable=False)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)
    thumbnail = models.FileField(upload_to='videos/thumbnails',null=True,blank=True)
    master_pl = models.FileField(upload_to='videos/master_playlist',null=True,blank=True)
    raw = models.FileField(upload_to='videos/raw_video')
    tags = models.TextField(max_length=500,null=True,blank=True)
    uploaded = models.DateTimeField(default=timezone.now)
    def toJson(self)->dict:
        data = {
            'title':self.title,
            'uniqueName':self.uniqueName,
            'courseName':self.course.title,
            'courseId':self.course.id,
            'thumbnail':self.thumbnail.path,
        }
        return data
    
    def __str__(self):
        return self.title