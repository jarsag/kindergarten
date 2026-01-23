from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, LoginForm
from children.forms import ChildForm
from children.models import Child

def register(request):
    """Регистрация с возможностью добавить ребенка (упрощенная форма)"""
    from children.forms import SimpleChildForm  # Используем упрощенную форму
    
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        child_form = SimpleChildForm(request.POST)  # Упрощенная форма
        
        if user_form.is_valid():
            # Создаем пользователя
            user = user_form.save()
            
            # Если указано имя ребенка, создаем его
            if child_form.is_valid() and child_form.cleaned_data.get('first_name'):
                child = child_form.save(commit=False)
                child.parent = user
                child.last_name = user.last_name  # Используем фамилию родителя
                child.save()
            
            # Логиним пользователя
            login(request, user)
            messages.success(request, f'Регистрация успешна! Добро пожаловать, {user.first_name}!')
            return redirect('profile')
    else:
        user_form = CustomUserCreationForm()
        child_form = SimpleChildForm()
    
    return render(request, 'accounts/register.html', {
        'form': user_form,
        'child_form': child_form,  # Передаем упрощенную форму
    })

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
    """Личный кабинет с детьми"""
    children = request.user.children.all()
    child_form = ChildForm()
    
    return render(request, 'accounts/profile.html', {
        'children': children,
        'child_form': child_form,
    })

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

@login_required
def add_child(request):
    """Добавление ребенка через форму"""
    if request.method == 'POST':
        try:
            from children.models import Child
            
            # Создаем ребенка
            child = Child.objects.create(
                parent=request.user,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                birth_date=request.POST.get('birth_date'),
                group=request.POST.get('group', ''),
                allergies=request.POST.get('allergies', ''),
                medical_notes=request.POST.get('medical_notes', ''),
            )
            
            # Обработка фото если есть
            if 'photo' in request.FILES:
                child.photo = request.FILES['photo']
                child.save()
            
            messages.success(request, f'Ребенок {child.first_name} успешно добавлен!')
            
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении ребенка: {str(e)}')
    
    return redirect('profile')

@login_required
def edit_child(request, child_id):
    """Редактирование ребенка"""
    child = get_object_or_404(Child, id=child_id, parent=request.user)
    
    if request.method == 'POST':
        form = ChildForm(request.POST, request.FILES, instance=child)
        if form.is_valid():
            form.save()
            messages.success(request, f'Данные ребенка {child.first_name} обновлены!')
            return redirect('profile')
    else:
        form = ChildForm(instance=child)
    
    return render(request, 'accounts/edit_child.html', {
        'form': form,
        'child': child
    })

@login_required
def delete_child(request, child_id):
    """Удаление ребенка"""
    child = get_object_or_404(Child, id=child_id, parent=request.user)
    
    if request.method == 'POST':
        child_name = child.first_name
        child.delete()
        messages.success(request, f'Ребенок {child_name} удален')
        return redirect('profile')
    
    return render(request, 'accounts/confirm_delete.html', {'child': child})
