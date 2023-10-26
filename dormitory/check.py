from main.tools import getTime

# Database Import
from main.models import Student
from .models import DormStatus

# Check Status Function
def dorm_status_check(studentID, time_get):
    # Const variable
    limit_time = 15

    student = Student.objects.get(studentID=studentID)

    # Get Year for defind limit_time
    year = int(student.class_name[0])
    if year <= 3:
        limit_time = 21*60
    else:
        limit_time = 23*60

    # Get current date
    date_now = getTime()["date"]
    
    data_respond = {
        "date": date_now,
        "status": None,
        "status_key" : None,
    }

    # Checking status
    if time_get <= limit_time:
        status = "T"
    else:
        status = "D"

    status = DormStatus.objects.get(status_key=status)
    data_respond["status"] = status.status_name
    data_respond["status_key"] = status.status_key

    return data_respond