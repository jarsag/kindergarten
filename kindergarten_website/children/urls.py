from django.urls import path
from . import views

urlpatterns = [
    # ... существующие пути ...
    path('child/<int:child_id>/edit/', views.edit_child, name='edit_child'),
    path('child/<int:child_id>/delete/', views.delete_child, name='delete_child'),
]