from django.db import models

# Create your models here.
class Admintable(models.Model):
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=50)


class University(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)