from django.urls import path
from . import views

urlpatterns = [
    path('', views.groups_list, name='groups_list'),
    path('<int:pk>/', views.group_detail, name='group_detail'),
]