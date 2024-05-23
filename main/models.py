import uuid
from django.db import models
from datetime import datetime
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=250)
    type = models.CharField(max_length=25)
    uniqueName = models.UUIDField(default=uuid.uuid4)
    price = models.IntegerField(default=0)
    uploadDate = models.DateTimeField(default='django.utils.timezone.now')
    
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
    uniqueName = models.UUIDField(default=uuid.uuid4)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)
    thumbnail = models.FileField(upload_to='videos/thumbnails',null=True)
    master_pl = models.FileField(upload_to='videos/master_playlist',null=True)
    raw = models.FileField(upload_to='videos/raw_video')
    tags = models.TextField(max_length=500,null=True,blank=True)
    
    def __str__(self):
        return self.title