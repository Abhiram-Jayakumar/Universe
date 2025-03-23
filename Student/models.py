from django.db import models
from django.utils.timezone import now

from Admin.models import University
from College.models import Event, Student
# Create your models here.

class StudentEventPost(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to Student
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Link to Event
    caption = models.TextField(blank=True, null=True)  # Caption for the post
    image = models.ImageField(upload_to="student_event_posts/", blank=False, null=False)  # Event Image
    created_at = models.DateTimeField(default=now)  # Timestamp of post creation
    is_approved = models.BooleanField(default=False)  # Whether the college has approved the post


class EventRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to Student
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Link to Event
    name = models.CharField(max_length=100)  # Name of the student
    email = models.EmailField()  # Email of the student
    phone = models.CharField(max_length=15)  # Contact number
    registered_at = models.DateTimeField(default=now)  # Timestamp of registration
    has_paid = models.BooleanField(default=False)  # Whether the payment is completed



class StudentNote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to="notes/", help_text="Upload PDF, Word, or Image")
    uploaded_at = models.DateTimeField(auto_now_add=True)