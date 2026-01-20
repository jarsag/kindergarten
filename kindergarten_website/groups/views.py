from django.shortcuts import render
from .models import Group

def groups_list(request):
    groups = Group.objects.all().order_by('age_range')
    return render(request, 'groups/list.html', {'groups': groups})

def group_detail(request, pk):
    group = Group.objects.get(pk=pk)
    return render(request, 'groups/detail.html', {'group': group})