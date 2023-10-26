from main.tools import get_timetable, getTime

# Database Import
from main.models import Student, TimeTable
from .models import ClassStatus, ClassRecord

# Check Status Function
def class_status_check(studentID, time_get):
    # Const variable
    limit_time = 15

    student = Student.objects.get(studentID=studentID)
    class_name = student.class_name

    # Get current time, date
    time_now, x, date_now, today = getTime().values()

    # Get timetable
    classtable = TimeTable.objects.filter(class_name=class_name, day=today)
    if classtable.count() == 0:
        return False
    
    table = get_timetable(classtable, time_now)

    if not table:
        return False

    period = table["period"]
    subj_name = table["subj"]
    time_start = table["time_start"]
    time_end = table["time_end"]

    data_respond = {
        "date": date_now,
        "period": period,
        "subject": subj_name,
        "status": None,
        "status_key": None,
    }

    # Check if student has already check-in
    record = ClassRecord.objects.filter(student=student, date=date_now, period=period).first()
    if record is None:
        check_in = True
    else:
        check_in = False

    # Checking status
    if check_in:
        if time_get <= time_start:
            status = "T"
        elif time_get <= time_start + limit_time:
            status = "D"
        else:
            status = "A"

    else:
        exist_status = record.status.status_key
        if time_get <= time_end - limit_time and exist_status not in ("D", "A", "O"):
            status = "L"
        else:
            data_respond["status"] = exist_status
            return data_respond

    status = ClassStatus.objects.get(status_key=status)
    data_respond["status"] = status.status_name
    data_respond["status_key"] = status.status_key

    return data_respond