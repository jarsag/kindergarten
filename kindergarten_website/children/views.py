from django.shortcuts import get_object_or_404
from children.models import Child
from children.forms import ChildForm

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