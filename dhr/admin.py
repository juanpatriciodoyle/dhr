from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

# Register your models here.
from dhr.models import Employee

admin.site.register(get_user_model())
admin.site.register(Employee)
