from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

# In App Import
from .serializers import studentSerializer, UserSerializer
from main.tools import getTime
from .security import encrypt

# Database Import 
from main.models import Student, TimeTable
from classroom.models import ClassStatus, ClassRecord
from dormitory.models import DormStatus, DormRecord
from student.models import Queue

# Status Check Function
from classroom.check import class_status_check
from dormitory.check import dorm_status_check

# ------ Authentication Part ------
# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = User.objects.get(username=request.data['username'])
#         user.set_password(request.data['password'])
#         user.save()
#         token = Token.objects.create(user=user)
#         return Response({'token': token.key, 'user': serializer.data})
#     return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response(f"passed for {request.user.username}")
    
# ------ Receive Data in JSON Format ------
@api_view(['GET', 'POST'])
def student_list(request, format=None):
    if request.method == 'GET':
        stu = Student.objects.all()
        serializer = studentSerializer(stu, many=True)
        return JsonResponse({'students':serializer.data})
    
    if request.method == 'POST':
        serializer = studentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors)

@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, id, format=None):
    stu = Student.objects.filter(studentID=id)
    if len(stu) == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    stu = stu.first()
    
    if request.method == 'GET':
        serializer = studentSerializer(stu)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = studentSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        stu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def student_table_class(request, class_name, period):

    x, x, date_now, today = getTime().values()

    student_list = Student.objects.filter(class_name=class_name).order_by('studentID')
    records = ClassRecord.objects.filter(date=date_now, period=period).order_by('student__studentID')
    student_status_list = {"student_list": [],
                           "timetable": [],
                           "all_status": [],}

    for student in student_list:
        student_json = {
            "studentID": student.studentID,
            "name": student.name,
            "status": "None",
            "status_key": "N",
            "status_color": "#8e9aaf",
        }

        if records.filter(student=student).count() != 0:
            student = records.filter(student=student).first()
            student_json["status"] = student.status.status_name
            student_json["status_key"] = student.status.status_key
            student_json["status_color"] = student.status.color

        student_status_list["student_list"].append(student_json)

    timetable_list = TimeTable.objects.filter(class_name=class_name, day=today)
    for subj in timetable_list:
        student_status_list["timetable"].append({
            "subj_name": subj.subject_name,
            "period": subj.period,
        })

    for st in ClassStatus.objects.all():
        student_status_list["all_status"].append({
            "status_key": st.status_key,
            "status_name": st.status_name,
        })

    return Response(student_status_list, status=status.HTTP_200_OK)

@api_view(['GET'])
def student_table_dorm(request, dorm_building):

    date_now = getTime()['date']

    student_list = Student.objects.filter(dorm_building=dorm_building).order_by('studentID')
    records = DormRecord.objects.filter(date=date_now).order_by('student__studentID')
    student_status_list = {"student_list": [],
                           "all_status": [],}

    for student in student_list:
        student_json = {
            "studentID": student.studentID,
            "name": student.name,
            "status": "None",
            "status_key": "N",
            "status_color": "#8e9aaf",
        }

        if student.dorm_room == "None":
            student_json["room"] = f"{student.dorm_building}-000"
        else:
            student_json["room"] = f"{student.dorm_building}-{student.dorm_room}"

        if records.filter(student=student).count() != 0:
            student = records.filter(student=student).first()
            student_json["status"] = student.status.status_name
            student_json["status_key"] = student.status.status_key
            student_json["status_color"] = student.status.color
        
        student_status_list["student_list"].append(student_json)

    for st in DormStatus.objects.all():
        student_status_list["all_status"].append({
            "key": st.status_key,
            "name": st.status_name,
        })

    return Response(student_status_list, status=status.HTTP_200_OK)


# ------ API Check Handle ------
# Classroom Check
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def class_check_handle(request):
    studentID = request.data['studentID']

    time_get, time_text, x, x = getTime().values()

    data_response = class_status_check(studentID, time_get)

    if not data_response:
        return  Response({"status": "No Timetable Found."}, status=status.HTTP_204_NO_CONTENT)

    date = data_response["date"]
    period = data_response["period"]
    status_record = data_response["status_key"]

    queue = Queue.objects.filter(type_q="class", student=Student.objects.get(studentID=studentID), date=date).first()
    if queue is None:
        queueID = encrypt(f"{status_record},{period},{studentID},{time_text}")
        queue = Queue(type_q="class", student= Student.objects.get(studentID=studentID), queueID=queueID, date=date, timeStamp=time_get)
        queue.save()
        
    else:
        queue.queueID = encrypt(f"{status_record},{period},{studentID},{time_text}")
        queue.timeStamp = time_get
        queue.save()

    return  Response(data_response, status=status.HTTP_200_OK)

# Dormitory Check
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def dorm_check_handle(request):
    studentID = request.data['studentID']

    time_get, time_text, x, x = getTime().values()

    data_response = dorm_status_check(studentID, time_get)

    date = data_response["date"]
    status_record = data_response["status_key"]

    queue = Queue.objects.filter(type_q="dorm", student=Student.objects.get(studentID=studentID)).first()
    if queue is None:
        queueID = encrypt(f"{status_record},{studentID},{time_text}")
        queue = Queue(type_q="dorm", student= Student.objects.get(studentID=studentID), queueID=queueID, date=date, timeStamp=time_get)
        queue.save()

    else:
        queue.queueID = encrypt(f"{status_record},{studentID},{time_text}")
        queue.timeStamp = time_get
        queue.save()

    return  Response(data_response, status=status.HTTP_200_OK)
