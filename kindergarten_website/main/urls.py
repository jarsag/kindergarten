from django.urls import path, include
from . import views
from .views import HomeView, AboutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('groups/', include('groups.urls')),
    path('contacts/', views.contacts, name='contacts'), 
]