from django.shortcuts import HttpResponse
import pandas as pd

from .models import Student, TimeTable
from classroom.models import ClassStatus
from dormitory.models import DormStatus

# Create your views here.
def import_student(request):
    df = pd.read_csv(r"static\csv\student_list.csv")

    for _, student in df.iterrows():
        try:
            Student.objects.get(studentID=student['studentID'])
            continue
        except:
            pass

        stu = Student(studentID=student['studentID'], name=student['name'], class_name=student['class_name'], dorm_building=student['dorm_building'], dorm_room=student['dorm_room'])
        stu.save()

    return HttpResponse("Import student success")

def import_timetable(request, class_name='3C2'):
    file_path = r"static\csv\timetable"
    file_path += f"\{class_name}.csv"
    df = pd.read_csv(file_path)

    for _, row in df.iterrows():
        try:
            TimeTable.objects.get(class_name=row['CLASS_NAME'], day=row['DAY'], period=row['PERIOD'])
            continue
        except:
            pass

        # print(row)
        # print(f"/nType time: {type(row['PERIOD'])}")
        # print('------------------')
        timetable = TimeTable(class_name=class_name, day=row['DAY'], period=row['PERIOD'], subject_name=row['SUBJECT_NAME'], time_start=row['TIME_START'], time_end=row['TIME_END'])
        timetable.save()

    return HttpResponse("Import timetable success")

def import_class_status(request):
    df = pd.read_csv(r"static\csv\class_status.csv")

    for _, status in df.iterrows():
        try:
            ClassStatus.objects.get(status_key=status['key'])
            continue
        except:
            pass

        stu = ClassStatus(status_key=status['key'], status_name=status['name'])
        stu.save()

    return HttpResponse("Import class status success")

def import_dorm_status(request):
    df = pd.read_csv(r"static\csv\dorm_status.csv")

    for _, status in df.iterrows():
        try:
            DormStatus.objects.get(status_key=status['key'])
            continue
        except:
            pass

        stu = DormStatus(status_key=status['key'], status_name=status['name'])
        stu.save()

    return HttpResponse("Import dorm status success")