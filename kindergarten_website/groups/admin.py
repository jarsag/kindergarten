from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'age_range', 'teacher', 'capacity', 'occupied')
    list_filter = ('age_range', 'has_pool')  # Убираем has_english, его нет в модели
    search_fields = ('name', 'teacher', 'description')