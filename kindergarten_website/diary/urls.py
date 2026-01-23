from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.diary_dashboard, name='dashboard'),
    path('child/<int:child_id>/', views.child_diary, name='child_diary'),
    path('child/<int:child_id>/add/', views.add_diary_entry, name='add_entry'),
    path('entry/<int:entry_id>/', views.view_entry, name='view_entry'),
]