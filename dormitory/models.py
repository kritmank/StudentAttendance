from django.db import models
from main.models import Student

# Create your models here.
class DormStatus(models.Model):
    status_key = models.CharField(max_length=2, primary_key=True)
    status_name = models.CharField(max_length=20, null=True)
    color = models.CharField(max_length=7, null=True)

    def __str__(self):
        return self.status_name
    
class DormRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.CharField(max_length=5, null=True)
    status = models.ForeignKey(DormStatus, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.student.studentID} {self.date} Status: {self.status}"