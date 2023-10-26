from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('map/', views.map),
    path('add-user/', views.addUser),
    path('add-info/', views.addInfo),
    path('check-queue/<queueID>', views.checkQueue),
    path('qrcode/<studentID>.png', views.studentQR_gen),
    path('edit-info/<studentID>', views.editInfo),
]