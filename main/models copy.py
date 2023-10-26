from django.db import models

# Create your models here.
class_choice = (
        ('3C1', '3C1'),
        ('3C2', '3C2'),
    )
dorm_choice = (
    ('7', 'Building 7'),
    ('8', 'Building 8'),
    ('N', 'None')
)

class TimeTable(models.Model):
    class_name = models.CharField(max_length=3, choices=class_choice, default='3C2')
    day = models.CharField(max_length=10, null=True)
    period = models.IntegerField(default=0, null=True)
    subject_name = models.CharField(max_length=100, null=True)
    time_start = models.CharField(max_length=5, null=True)
    time_end = models.CharField(max_length=5, null=True)

    def __str__(self):
        return f"{self.class_name} : {self.day} {self.period}"
    
# ------ Student ------
class Student(models.Model):
    studentID=models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=50, default='None')
    class_name = models.CharField(choices=class_choice, null=True)
    dorm_building = models.CharField(choices=dorm_choice, null=True)
    dorm_room = models.CharField(max_length=4, default="None")

    def __str__(self):
        return self.studentID

    
