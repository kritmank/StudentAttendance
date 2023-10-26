from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Database Import
from main.models import Student, TimeTable
from .models import ClassStatus, ClassRecord

# Library Import
from main.tools import http_method_check, get_timetable, getTime


""" Index Page """
@login_required(login_url='/auth/login')
def classroom(request, class_name):
    res = http_method_check(request.method, ["GET"])
    if res:
        return JsonResponse(res, status=404)
    
    if request.method == "POST":
        return classroom_change_status(request)
    
    class_name = class_name.upper()
    time_now, x, date_now, today = getTime().values()

    param = {
        "Today": date_now,
        "today_name": today,
        "class_name": class_name,
        "subj_name": "None",
        "period": 0,
    }

    # Weekends
    if today in ("SAT", "SUN"):
        return render(request, "class.html", param)
    
    classtable = TimeTable.objects.filter(class_name=class_name, day=today)
    if classtable.first() is None:
        return HttpResponse("No timetable.", status=200)

    table = get_timetable(classtable, time_now)
    if not table:
        return HttpResponse("Timetable Error.", status=200)

    period = table["period"]
    subj_name = table["subj"]

    param["subj_name"] = subj_name
    param["period"] = period

    return render(request, "class.html", param)


""" Change Status Handler """
@csrf_exempt
def classroom_change_status(request):
    res = http_method_check(request.method, ["POST"])
    if res:
        return JsonResponse(res, status=404)
    
    date_now = getTime()["date"]

    studentID = request.POST.get("ID")
    period = int(request.POST.get("periodChange"))
    status = request.POST.get("statusChange")
    stu = Student.objects.get(studentID=studentID)

    stu_save = ClassRecord.objects.filter(student=stu, date=date_now, period=period)
    if stu_save.count() == 0:
        stu_save = ClassRecord(student=stu, date=date_now, period=period)
    else:
        stu_save = stu_save.first()

    stu_save.status = ClassStatus.objects.get(status_key=status)
    stu_save.save()

    return redirect(f"/class/table/{stu.class_name}/")