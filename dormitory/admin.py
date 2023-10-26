from django.contrib import admin
from .models import DormStatus, DormRecord

# Register your models here.
admin.site.register(DormStatus)
admin.site.register(DormRecord)
