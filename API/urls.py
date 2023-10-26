from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # path('', views.index),
    # path('signup/', views.signup),
    # path('test_token/', views.test_token),
    
    # ------ Authen Path ------
    path('login/', views.login),
    path('student/', views.student_list),
    path('student/<int:id>', views.student_detail),
    path('class-check/', views.class_check_handle),
    path('dorm-check/', views.dorm_check_handle),

    # AJAX
    path('classroom/<str:class_name>/<int:period>/', views.student_table_class),
    path('dorm/<str:dorm_building>/', views.student_table_dorm),
]

urlpatterns = format_suffix_patterns(urlpatterns)
