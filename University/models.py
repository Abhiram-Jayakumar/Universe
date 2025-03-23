from django.db import models

from Admin.models import University
from django.utils.timezone import now

# Create your models here.

class College(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.CASCADE) 
    
    
class Notification(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)  # Link to University
    title = models.CharField(max_length=200)  # Notification Title
    description = models.TextField()  # Detailed Notification Content
    created_at = models.DateTimeField(default=now)  # Timestamp
    is_active = models.BooleanField(default=True)  # Active/Inactive Notification
    file = models.FileField(upload_to="notifications/", blank=True, null=True)