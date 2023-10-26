from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('table/', lambda request: redirect('/class/table/3C2/')),
    path('table/<class_name>/', views.classroom),
    path('change-status/', views.classroom_change_status),
]