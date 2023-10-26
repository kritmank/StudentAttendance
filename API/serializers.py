from student.models import Student
from django.contrib.auth.models import User
from rest_framework import serializers

class studentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User 
        fields = ['id', 'username', 'password', 'email']