from django.db import models
from main.models import Student

# Create your models here.
class ClassStatus(models.Model):
    status_key = models.CharField(max_length=2, primary_key=True)
    status_name = models.CharField(max_length=20, null=True)
    color = models.CharField(max_length=7, null=True)

    def __str__(self):
        return self.status_name
    
class ClassRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.CharField(max_length=5, null=True)
    period = models.IntegerField(default=0)
    status = models.ForeignKey(ClassStatus, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.student.studentID} {self.date} Period: {self.period} Status: {self.status}"