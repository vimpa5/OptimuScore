from django.contrib import admin
from .models import MyRegistration
# Register your models here.

@admin.register(MyRegistration)
class MyRegistrationAdmin(admin.ModelAdmin):
    list_display=('username', 'email', 'first_name', 'last_name', 'location', 'designation')