from django.shortcuts import HttpResponse
import pandas as pd

from .models import Student

# Create your views here.
def export_student(request):
    student_list = Student.objects.all().order_by('studentID')
    dataFrame = {"studentID": [], "name": [], "class_name": [], "dorm_building": [], "dorm_room": []}
    for student in student_list:
        dataFrame["studentID"].append(student.studentID)
        dataFrame["name"].append(student.name)
        dataFrame["class_name"].append(student.class_name)
        dataFrame["dorm_building"].append(student.dorm_building)
        dataFrame["dorm_room"].append(student.dorm_room)
    
    df = pd.DataFrame(dataFrame)
    df.to_csv(r"static\csv\student_list.csv", index=False)
    return HttpResponse("Export student success")