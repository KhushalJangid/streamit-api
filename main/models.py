import uuid
from django.db import models
from datetime import datetime
# Create your models here.

class Course(models.Model):
    title = models.TextField()
    type = models.TextField()
    uniqueName = models.UUIDField(default=uuid.uuid4)
    price = models.IntegerField()
    uploadDate = models.DateTimeField(default='django.utils.timezone.now')
    
class VideoAsset(models.Model):
    title = models.TextField()
    uniqueName = models.UUIDField(default=uuid.uuid4)
    asset = models.FileField()