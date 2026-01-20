from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_main, name='gallery_main'),
    path('category/<slug:slug>/', views.gallery_category, name='gallery_category'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
]