# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 
                   'child_name', 'child_group', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'child_group')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'child_name')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar')}),
        ('Информация о ребенке', {'fields': ('child_name', 'child_age', 'child_group')}),
        ('Настройки уведомлений', {'fields': ('notification_email', 'notification_sms')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                     'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)