from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('table/', lambda request: redirect('/dorm/table/7/')),
    path('table/<dorm_building>/', views.dorm),
    path('change-status/', views.dorm_change_status),
]