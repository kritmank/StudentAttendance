from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Database Import
from main.models import Student
from .models import DormStatus, DormRecord

# Library Import
from main.tools import http_method_check, getTime


""" Index Page """
@login_required(login_url='/auth/login')
def dorm(request, dorm_building="7"):
    res = http_method_check(request.method, ["GET"])
    if res:
        return JsonResponse(res, status=404)

    dorm_building = dorm_building
    time_now, x, date_now, today = getTime().values()
    
    # print(f"Time now: {time_now}")

    return render(request, "dorm.html", {
        "Today": date_now,
        "today_name": today,
        "dorm_building": dorm_building,
    })


""" Change Status Handler """
@csrf_exempt
def dorm_change_status(request):
    res = http_method_check(request.method, ["POST"])
    if res:
        return JsonResponse(res, status=404)

    date_now = getTime()["date"]

    studentID = request.POST.get("ID")
    status = request.POST.get("statusChange")
    print(f"studentID: {studentID}, status: {status}")
    stu = Student.objects.get(studentID=studentID)
    print(f"studentID: {studentID}, status: {status}")

    stu_save = DormRecord.objects.filter(student=stu, date=date_now)
    if stu_save.count() == 0:
        stu_save = DormRecord(student=stu, date=date_now)
    else:
        stu_save = stu_save.first()

    stu_save.status = DormStatus.objects.get(status_key=status)
    stu_save.save()

    return redirect(f"/dorm/table/{stu.dorm_building}/")