from django.contrib import admin
from .models import User, Queue

# Register your models here.
admin.site.register(User)
admin.site.register(Queue)