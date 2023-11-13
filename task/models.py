from django.db import models
from django.conf import settings
from user.models import BaseUser

# Create your models here.

class Task(models.Model):
    STATUS_CHOICE = [
        ('', 'Select Status'),
        ('created','Created'),
        ('inprogress','Inprogress'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]
   
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICE)
    assigned = models.ForeignKey(BaseUser,on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title