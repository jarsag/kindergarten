from django.db import models

class ParentDocument(models.Model):
    DOCUMENT_TYPES = [
        ('contract', 'Договор'),
        ('application', 'Заявление'),
        ('rules', 'Правила'),
        ('schedule', 'Расписание'),
        ('menu', 'Меню'),
        ('payment', 'Оплата'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название документа")
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, verbose_name="Тип документа")
    file = models.FileField(upload_to='parents/documents/', verbose_name="Файл")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    
    class Meta:
        verbose_name = "Документ для родителей"
        verbose_name_plural = "Документы для родителей"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_file_extension(self):
        import os
        return os.path.splitext(self.file.name)[1].upper().replace('.', '')

class ParentTip(models.Model):
    CATEGORIES = [
        ('health', 'Здоровье ребенка'),
        ('education', 'Воспитание и развитие'),
        ('adaptation', 'Адаптация к саду'),
        ('nutrition', 'Питание'),
        ('safety', 'Безопасность'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    category = models.CharField(max_length=50, choices=CATEGORIES, verbose_name="Категория")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to='parents/tips/', blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    class Meta:
        verbose_name = "Совет для родителей"
        verbose_name_plural = "Советы для родителей"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title