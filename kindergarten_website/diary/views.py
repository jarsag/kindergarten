from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from children.models import Child
from .models import DiaryEntry
from .forms import DiaryEntryForm

@login_required
def diary_dashboard(request):
    """Главная страница электронного дневника"""
    # Получаем детей текущего пользователя
    children = request.user.children.all()
    
    # Получаем последние записи для каждого ребенка
    child_entries = {}
    for child in children:
        entries = child.diary_entries.all()[:5]  # Последние 5 записей
        if entries.exists():
            child_entries[child] = entries
    
    return render(request, 'diary/dashboard.html', {
        'children': children,
        'child_entries': child_entries,
    })

@login_required
def child_diary(request, child_id):
    """Дневник конкретного ребенка"""
    child = get_object_or_404(Child, id=child_id, parent=request.user)
    entries = child.diary_entries.all().order_by('-date')
    
    return render(request, 'diary/child_diary.html', {
        'child': child,
        'entries': entries,
    })

@login_required
def add_diary_entry(request, child_id):
    """Добавление записи в дневник"""
    child = get_object_or_404(Child, id=child_id, parent=request.user)
    
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.child = child
            entry.save()
            messages.success(request, f'Запись в дневник {child.first_name} добавлена!')
            # ИСПРАВЛЕНО: добавлен namespace 'diary:'
            return redirect('diary:child_diary', child_id=child_id)
    else:
        form = DiaryEntryForm()
    
    return render(request, 'diary/add_entry.html', {
        'form': form,
        'child': child,
    })

@login_required
def view_entry(request, entry_id):
    """Просмотр конкретной записи"""
    entry = get_object_or_404(DiaryEntry, id=entry_id, child__parent=request.user)
    
    return render(request, 'diary/view_entry.html', {
        'entry': entry,
    })

@login_required
def delete_diary_entry(request, entry_id):
    """Удаление записи из дневника"""
    entry = get_object_or_404(DiaryEntry, id=entry_id, child__parent=request.user)
    child_id = entry.child.id
    
    if request.method == 'POST':
        child_name = entry.child.first_name
        entry_date = entry.date
        entry.delete()
        
        messages.success(request, f'Запись от {entry_date.strftime("%d.%m.%Y")} удалена из дневника {child_name}')
        return redirect('diary:child_diary', child_id=child_id)
    
    # Если GET запрос - показываем страницу подтверждения
    return render(request, 'diary/confirm_delete_entry.html', {
        'entry': entry,
    })

@login_required
def edit_diary_entry(request, entry_id):
    """Редактирование записи в дневнике"""
    entry = get_object_or_404(DiaryEntry, id=entry_id, child__parent=request.user)
    
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, f'Запись от {entry.date.strftime("%d.%m.%Y")} обновлена!')
            return redirect('diary:view_entry', entry_id=entry_id)
    else:
        form = DiaryEntryForm(instance=entry)
    
    return render(request, 'diary/edit_entry.html', {
        'form': form,
        'entry': entry,
        'child': entry.child,
    })