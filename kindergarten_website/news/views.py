from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News

def news_list(request):
    news_list = News.objects.filter(is_published=True).order_by('-published_date')
    
    # Пагинация
    paginator = Paginator(news_list, 6)  # 6 новостей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': News.CATEGORY_CHOICES,
    }
    return render(request, 'news/list.html', context)

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug, is_published=True)
    news.increase_views()  # Увеличиваем счетчик просмотров
    
    # Получаем похожие новости
    similar_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id).order_by('-published_date')[:3]
    
    context = {
        'news': news,
        'similar_news': similar_news,
    }
    return render(request, 'news/detail.html', context)

def news_by_category(request, category):
    news_list = News.objects.filter(
        category=category,
        is_published=True
    ).order_by('-published_date')
    
    paginator = Paginator(news_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    category_name = dict(News.CATEGORY_CHOICES).get(category, category)
    
    context = {
        'page_obj': page_obj,
        'categories': News.CATEGORY_CHOICES,
        'current_category': category,
        'category_name': category_name,
    }
    return render(request, 'news/list.html', context)