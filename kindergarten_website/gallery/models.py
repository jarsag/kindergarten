from django.db import models
from django.utils import timezone

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True, null=True, verbose_name="Обложка")
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Категория галереи"
        verbose_name_plural = "Категории галереи"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('gallery_category', args=[self.slug])
    
    def photo_count(self):
        return self.photos.filter(is_active=True).count()

class GalleryPhoto(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, 
                                 related_name='photos', verbose_name="Категория")
    image = models.ImageField(upload_to='gallery/photos/%Y/%m/', verbose_name="Фотография")
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="Дата загрузки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    
    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('photo_detail', args=[self.id])
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_next_photo(self):
        next_photo = GalleryPhoto.objects.filter(
            category=self.category,
            uploaded_at__gt=self.uploaded_at,
            is_active=True
        ).order_by('uploaded_at').first()
        return next_photo
    
    def get_prev_photo(self):
        prev_photo = GalleryPhoto.objects.filter(
            category=self.category,
            uploaded_at__lt=self.uploaded_at,
            is_active=True
        ).order_by('-uploaded_at').first()
        return prev_photo