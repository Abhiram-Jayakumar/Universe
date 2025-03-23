from django.db import models
from django.utils.timezone import now
from University.models import College
from datetime import datetime

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    college = models.ForeignKey(College, on_delete=models.CASCADE) 

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    
class Faculty(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    description = models.TextField() 
    social_media = models.URLField(max_length=200, blank=True, null=True)  
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
class Event(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)  # Link to College
    title = models.CharField(max_length=200)  # Event title
    description = models.TextField()  # Event description
    created_at = models.DateTimeField(default=now)  # Timestamp of event creation
    image = models.ImageField(upload_to="events/", blank=True, null=True)  # Optional event image
    is_active = models.BooleanField(default=True)  # Whether event is active or archived
    likes = models.PositiveIntegerField(default=0)  # Number of likes on the event post
    is_registration_required = models.BooleanField(default=False)  # Whether registration is required for the event
    is_registration_free = models.BooleanField(default=True)  # Whether registration is free
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Registration Fee

    def save(self, *args, **kwargs):
        """Ensure registration fee is required only when registration is not free."""
        if self.is_registration_required and not self.is_registration_free:
            if self.registration_fee is None:
                raise ValueError("Registration fee must be provided if registration is not free.")
        else:
            self.registration_fee = None  # Reset fee if registration is free
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    
class Placement(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)  # Link to the college
    job_title = models.CharField(max_length=200)  # Job title
    company_name = models.CharField(max_length=200)  # Company name
    job_description = models.TextField()  # Detailed description of the job
    skills_required = models.TextField()  # Skills required for the job
    application_deadline = models.DateTimeField()  # Application deadline
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional salary info
    is_active = models.BooleanField(default=True)  # Whether the job opportunity is still open
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the placement was added
    image = models.ImageField(upload_to="placements/", blank=True, null=True)  # Image for the advertisement

    def save(self, *args, **kwargs):
        # Automatically set 'is_active' to False if the application deadline has passed
        if self.application_deadline < datetime.now():
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    class Meta:
        ordering = ['-created_at']