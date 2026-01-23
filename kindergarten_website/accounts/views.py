from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, LoginForm

def register(request):
    """Регистрация с автоматическим username из email если не указан"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Регистрация успешна! Добро пожаловать, {user.first_name}!')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Вход по email ИЛИ username - УНИВЕРСАЛЬНЫЙ"""
    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        User = get_user_model()
        user = None
        
        if '@' in identifier:  # Если ввод похож на email
            try:
                # Ищем пользователя по email
                user_by_email = User.objects.get(email=identifier)
                # Пробуем аутентифицировать с username из базы
                user = authenticate(request, username=user_by_email.username, password=password)
            except User.DoesNotExist:
                pass
        
        # Если не нашли по email или это не email, пробуем как username
        if user is None:
            user = authenticate(request, username=identifier, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name}!')
            return redirect('profile')
        else:
            messages.error(request, 'Неверный email/логин или пароль')
    
    # Для GET запроса или неудачной аутентификации
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('home')

@login_required
def profile(request):
    """Личный кабинет пользователя"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    """Редактирование профиля"""
    # Временно закомментируем, пока нет CustomUserChangeForm
    messages.info(request, 'Редактирование профиля скоро будет доступно')
    return redirect('profile')
    """
    # Раскомментировать когда создадите CustomUserChangeForm
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})
    """