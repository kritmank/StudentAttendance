from django.shortcuts import HttpResponse, render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

import qrcode

# App Function
from API.security import encryptQR, decrypt
from main.tools import http_method_check, getTime
from .smtp_send import send_email

# Database
from .models import User, Queue
from main.models import Student
from classroom.models import ClassStatus, ClassRecord
from dormitory.models import DormStatus, DormRecord

# Create your views here.
@csrf_exempt
def index(request):
    res = http_method_check(request.method, ["GET", "POST"])
    if res:
        return JsonResponse(res, status=404)
    
    if request.method == "GET":
        return render(request, 'student_app/loading.html')
    
    userID = request.POST.get('userID')
    student = User.objects.filter(userID=userID).first()

    if student is None:
        return render(request, 'student_app/id_register.html', {'userID': userID})
    
    time_now, x, date_now, x = getTime().values()

    student = student.student
    queue = Queue.objects.filter(student=student, date=date_now)
    queue_list = []

    if len(queue) > 2:
        for q in queue:
            q.delete()
    elif len(queue) != 0:
        for q in queue:
            time_limit = 2 
            timeStamp =  q.timeStamp
            if time_now - timeStamp > time_limit:
                queue.delete()
            else:
                queue_list.append(q)

    queue_status = False if len(queue_list) == 0 else True
    
    return render(request, 'student_app/profile.html', {'student': student, 
                                                    'queue_status': queue_status,
                                                    'queue_list': queue_list})

@csrf_exempt
def addUser(request):
    res = http_method_check(request.method, ["POST"])
    if res:
        return JsonResponse(res, status=404)
    
    studentID = request.POST.get('studentID')
    userID = request.POST.get('userID')

    student = Student.objects.filter(studentID=studentID).first()
    if student is None or student.name == "None" or student.dorm_room == "None" or student.dorm_building == "None":
        return render(request, 'student_app/info_register.html', {'studentID': studentID, 
                                                                  'userID': userID})

    user = User.objects.filter(student=student)
    if user.count() != 0:
        messages.error(request, "User Already Exist")
        return HttpResponseRedirect("/student/")

    user = User(userID=userID, student=student)
    user.save()

    return redirect('/student/')

@csrf_exempt
def addInfo(request):
    res = http_method_check(request.method, ["POST"])
    if res:
        return JsonResponse(res, status=404)
    
    studentID = request.POST.get('studentID')
    userID = request.POST.get('userID')
    name = request.POST.get('name')
    dorm, room = request.POST.get('dorm').split("-")
    class_name = request.POST.get('class')

    student = Student(studentID=studentID, name=name, dorm_building=dorm, dorm_room=room, class_name=class_name)
    student.save()

    user = User.objects.filter(student=student)
    if user.count() != 0:
        messages.error(request, "User Already Exist")
        return HttpResponseRedirect("/student/")

    user = User(userID=userID, student=student)
    user.save()

    return redirect('/student/')

def map(request):
    return render(request, 'student_app/map.html')

@csrf_exempt
def checkQueue(request, queueID):
    res = http_method_check(request.method, ["POST"])
    if res:
        return JsonResponse(res, status=404)
    
    # Get Data from POST
    studentID = request.POST.get('studentID')
    student = Student.objects.get(studentID=studentID)
    queue = Queue.objects.filter(queueID=queueID).first()

    if queue is None:
        render(request, 'student_app/error.html', 
                    {'message1': "Queue Not Found!",
                    'message2': "Please Scan ID Again.",})

    time_limit = 2
    time_now, time_text, x, x = getTime().values()

    # Check Exception
    if queue.student != student:
        queue.delete()
        return render(request, 'student_app/error.html', 
                    {'message1': "StudentID Not Match!",
                    'message2': "Please Scan ID Again.",})
    
    elif time_now - queue.timeStamp > time_limit:
        queue.delete()
        return render(request, 'student_app/error.html', 
                    {'message1': "Request Time Out!",
                    'message2': "Please Scan ID Again.",})
    
    if queue.type_q not in ("class", "dorm"):
        return HttpResponse(status=404)

    lat = float(request.POST.get('lat'))
    long = float(request.POST.get('long'))
    # print(f"Lat: {lat} Long: {long}")

    queueID = decrypt(queue.queueID)
    if queue.type_q == "class":
        # Checking Location
        if not ((13.72611 < lat < 13.72715) and (100.77845 < long < 100.78012)):
            return render(request, 'student_app/unsuccess.html')
        
        status, period, studentID, time = queueID.split(",")
        status = ClassStatus.objects.get(status_key=status)
        record = ClassRecord.objects.filter(student=student, date=queue.date, period=period).first()
        if record is None:
            record = ClassRecord(student=student, date=queue.date, time=time, period=period, status=status)
            record.save()

        else:
            record.status = status
            record.save()

    elif queue.type_q == "dorm":
        if not ((13.72942 < lat < 13.72990) and (100.77442 < long < 100.77501)):
            return render(request, 'student_app/unsuccess.html')
        
        status, studentID, time = queueID.split(",")
        status = DormStatus.objects.get(status_key=status)
        record = DormRecord.objects.filter(student=student, date=queue.date).first()
        if record is None:
            record = DormRecord(student=student, date=queue.date, time=time, status=status)
            record.save()
        
        else:
            record.status = status
            record.save()

    queue.delete()
    send_email(student, queue.type_q, status.status_name, time_text)
    return render(request, 'student_app/success.html')
        

def studentQR_gen(request, studentID):
    res = http_method_check(request.method, ["GET"])
    if res:
        return JsonResponse(res, status=404)
    
    student = Student.objects.filter(studentID=studentID).first()
    if student is None:
        return HttpResponse("Student not in database.", status=404)
    
    data =  encryptQR(f"{studentID}")
    img = qrcode.make(data)

    respond = HttpResponse(content_type="image/png")
    img.save(respond, "PNG")

    return respond

@csrf_exempt
def editInfo(request, studentID):
    student = Student.objects.get(studentID=studentID)
    
    name = request.POST.get('name')
    building, room = request.POST.get('dorm').split("-")
    class_name = request.POST.get('class')

    student.name = name
    student.dorm_building = building
    student.dorm_room = room
    student.save()

    return redirect('/student/')

# @csrf_exempt
# def id_register(request):
#     if request.method == "POST":
#         studentID = request.POST.get('studentID')
#         UserID = request.POST.get('userID')
#         student_obj = Student.objects.get(studentID=studentID)
#         print(student_obj.name, student_obj.class_name, student_obj.dorm_room, student_obj.dorm_building) 
#         if student_obj.name == "None" or student_obj.dorm_room == "None" or student_obj.dorm_building == "None":
#             return render(request, 'student_app/info_register.html', {
#                 'studentID': studentID,
#                 'userID': UserID,
#             })
#         else:
#             return redirect('/student')

#     return render(request, 'student_app/id_register.html')


# @csrf_exempt
# def info_register(request):
#     if request.method == "POST":
#         studentID = request.POST.get('studentID')
#         UserID = request.POST.get('userID')

#         name = request.POST.get('name')
#         dorm = request.POST.get('dorm')
#         class_name = request.POST.get('class')

#         dorm_list = dorm.split("-")

#         student_obj = Student.objects.get(studentID=studentID)

#         if(student_obj):
#             student_obj.name = name
#             student_obj.dorm_building = dorm_list[0]
#             student_obj.dorm_room = dorm_list[1]
#             student_obj.class_name = class_name
#             student_obj.save()
#             return redirect('/student')
#         else:
#             student = Student(studentID=studentID, name=name, dorm_building=dorm_list[0], dorm_room=dorm_list[1], class_name=class_name)
#             student.save()
#             return redirect('/student')


#     return render(request, 'student_app/info_register.html')
