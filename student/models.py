from django.db import models

# Database Import
from main.models import Student

# Create your models here.
class User(models.Model):
    userID = models.CharField(max_length=40, primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.student}: {self.userID}"
    
class Queue(models.Model):
    queueID = models.CharField(max_length=100, primary_key=True)
    type_q = models.CharField(max_length=10, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    timeStamp = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.queueID}"