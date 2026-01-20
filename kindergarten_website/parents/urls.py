from django.urls import path
from . import views

urlpatterns = [
    path('', views.parents_main, name='parents_main'),
    path('tips/<str:category>/', views.tips_by_category, name='tips_by_category'),
]