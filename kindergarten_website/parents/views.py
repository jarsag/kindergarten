from django.shortcuts import render
from .models import ParentDocument, ParentTip

def parents_main(request):
    # Основные документы
    important_docs = ParentDocument.objects.filter(
        document_type__in=['contract', 'rules'],
        is_active=True
    )[:5]
    
    # Все документы по категориям
    docs_by_type = {}
    for doc_type, doc_name in ParentDocument.DOCUMENT_TYPES:
        docs = ParentDocument.objects.filter(
            document_type=doc_type,
            is_active=True
        )[:3]
        if docs:
            docs_by_type[doc_name] = docs
    
    # Советы для родителей
    tips = ParentTip.objects.filter(is_published=True).order_by('-created_at')[:6]
    
    context = {
        'title': 'Родителям',
        'important_docs': important_docs,
        'docs_by_type': docs_by_type,
        'tips': tips,
        'categories': ParentTip.CATEGORIES,
    }
    return render(request, 'parents/main.html', context)

def tips_by_category(request, category):
    tips = ParentTip.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')
    
    category_name = dict(ParentTip.CATEGORIES).get(category, category)
    
    context = {
        'title': f'Советы - {category_name}',
        'tips': tips,
        'current_category': category,
        'category_name': category_name,
        'categories': ParentTip.CATEGORIES,
    }
    return render(request, 'parents/tips.html', context)