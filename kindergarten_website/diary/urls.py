from django.urls import path
from . import views

app_name = 'diary'  # Пространство имен важно!

urlpatterns = [
    path('', views.diary_dashboard, name='dashboard'),
    path('child/<int:child_id>/', views.child_diary, name='child_diary'),
    path('child/<int:child_id>/add/', views.add_diary_entry, name='add_entry'),
    path('entry/<int:entry_id>/', views.view_entry, name='view_entry'),
    path('entry/<int:entry_id>/edit/', views.edit_diary_entry, name='edit_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_diary_entry, name='delete_entry'),
]