from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'main/home.html'

class AboutView(TemplateView):
    template_name = 'main/about.html'

# Простые функции-представления для совместимости
def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    context = {
        'title': 'Контакты',
        'contacts': {
            'address': 'г. Москва, ул. Детская, 123',
            'phone': '+7 (495) 123-45-67',
            'email': 'info@kindergarten.ru',
            'working_hours': 'Пн-Пт: 7:00 - 19:00, Сб-Вс: выходной',
            'director': 'Иванова Анна Петровна',
            'director_phone': '+7 (495) 123-45-68',
        }
    }
    return render(request, 'main/contacts.html', context)