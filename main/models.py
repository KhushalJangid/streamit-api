import uuid
from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    thumbnail = models.FileField(upload_to='courses/thumbnails',null=True,blank=True)
    type = models.CharField(max_length=25)
    uniqueName = models.UUIDField(default=uuid.uuid4,editable=False)
    price = models.IntegerField(default=0)
    uploadDate = models.DateTimeField(default=timezone.now)
    
    def toJson(self)->dict:
        js =  {
            "id":self.id,
            "title":self.title,
            "thumbnail":self.thumbnail.url,
            "description":self.description,
            "type":self.type,
            "uniqueName":self.uniqueName,
            "price":self.price,
            "uploadDate":self.uploadDate
        }
        return js
    def __str__(self) -> str:
        return self.title
    
class Wishlist(models.Model):
    user = models.ForeignKey(to='account.User',on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'course',)
    def __str__(self) -> str:
        return self.user.email
    
class VideoAsset(models.Model):
    title = models.CharField(max_length=250)
    uniqueName = models.UUIDField(default=uuid.uuid4,editable=False)
    course = models.ForeignKey(to=Course,on_delete=models.CASCADE)
    thumbnail = models.FileField(upload_to='videos/thumbnails',null=True,blank=True)
    master_pl = models.FileField(upload_to='videos/master_playlist',null=True,blank=True)
    raw = models.FileField(upload_to='videos/raw_video')
    aws_job_id = models.CharField(max_length=250)
    aws_job_status = models.CharField(max_length=10)
    tags = models.TextField(max_length=500,null=True,blank=True)
    uploaded = models.DateTimeField(default=timezone.now)
    def toJson(self)->dict:
        data = {
            'title':self.title,
            'uniqueName':self.uniqueName,
            'thumbnail':self.thumbnail.url,
            'uploadDate':self.uploaded,
        }
        return data
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        rawfile = self.raw
        super(VideoAsset, self).save(*args, **kwargs)