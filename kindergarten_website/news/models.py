from django.db import models
from django.utils import timezone

class News(models.Model):
    CATEGORY_CHOICES = [
        ('events', 'События'),
        ('announcements', 'Объявления'),
        ('tips', 'Советы родителям'),
        ('achievements', 'Достижения'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    content = models.TextField(verbose_name="Содержание")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='events', verbose_name="Категория")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Изображение")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('news_detail', args=[self.slug])
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])