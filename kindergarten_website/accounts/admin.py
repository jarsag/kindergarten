# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Импортируем модель Child если хотим показывать детей
from children.models import Child

class CustomUserAdmin(UserAdmin):
    # ИСПРАВЛЕННЫЙ list_display - убраны поля ребенка
    list_display = ('username', 'email', 'first_name', 'last_name', 
                   'phone', 'is_staff', 'is_active')
    
    # ИСПРАВЛЕННЫЙ list_filter - убрано child_group
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # ИСПРАВЛЕННЫЙ fieldsets - убрана секция "Информация о ребенке"
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar')}),
        ('Настройки уведомлений', {'fields': ('notification_email', 'notification_sms')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                     'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Опционально: добавим отображение количества детей
    def children_count(self, obj):
        return obj.children.count()  # Используем related_name из модели Child
    children_count.short_description = 'Количество детей'
    
    # Можно добавить children_count в list_display:
    # list_display = ('username', 'email', 'first_name', 'last_name', 
    #                'phone', 'children_count', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)