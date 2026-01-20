from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import GalleryCategory, GalleryPhoto

def gallery_main(request):
    categories = GalleryCategory.objects.filter(is_active=True).order_by('order')
    
    # Последние фотографии
    latest_photos = GalleryPhoto.objects.filter(
        is_active=True
    ).select_related('category').order_by('-uploaded_at')[:12]
    
    # Популярные фотографии
    popular_photos = GalleryPhoto.objects.filter(
        is_active=True
    ).order_by('-views')[:6]
    
    context = {
        'title': 'Галерея',
        'categories': categories,
        'latest_photos': latest_photos,
        'popular_photos': popular_photos,
    }
    return render(request, 'gallery/main.html', context)

def gallery_category(request, slug):
    category = get_object_or_404(GalleryCategory, slug=slug, is_active=True)
    photos = GalleryPhoto.objects.filter(
        category=category,
        is_active=True
    ).order_by('-uploaded_at')
    
    # Пагинация
    paginator = Paginator(photos, 12)  # 12 фото на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': f'Галерея - {category.name}',
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'gallery/category.html', context)

def photo_detail(request, pk):
    photo = get_object_or_404(GalleryPhoto, pk=pk, is_active=True)
    photo.increase_views()  # Увеличиваем счетчик просмотров
    
    # Похожие фото из той же категории
    similar_photos = GalleryPhoto.objects.filter(
        category=photo.category,
        is_active=True
    ).exclude(id=photo.id).order_by('-uploaded_at')[:4]
    
    # Навигация вперед/назад
    next_photo = photo.get_next_photo()
    prev_photo = photo.get_prev_photo()
    
    context = {
        'title': photo.title,
        'photo': photo,
        'similar_photos': similar_photos,
        'next_photo': next_photo,
        'prev_photo': prev_photo,
    }
    return render(request, 'gallery/detail.html', context)