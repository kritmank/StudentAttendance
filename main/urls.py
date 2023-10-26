from django.urls import path
from . import import_tool as imt
from . import export_tool as ext
from . import views

urlpatterns = [
    path('import_student/', imt.import_student, name='import_student'),
    path('import_timetable/', imt.import_timetable, name='import_timetable'),
    path('import_timetable/<class_name>', imt.import_timetable, name='import_timetable'),
    path('import_class_status/', imt.import_class_status, name='import_class_status'),
    path('import_dorm_status/', imt.import_dorm_status, name='import_dorm_status'),
    
    path('export_student/', ext.export_student, name='export_student'),
    path('', views.index),
]