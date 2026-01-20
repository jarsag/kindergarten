from django.db import models

class Application(models.Model):
    AGE_CHOICES = [
        ('', 'Не указано'),
        ('1.5-3', '1.5-3 года'),
        ('3-4', '3-4 года'),
        ('4-5', '4-5 лет'),
        ('5-6', '5-6 лет'),
        ('6-7', '6-7 лет'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя родителя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    child_age = models.CharField(max_length=10, choices=AGE_CHOICES, blank=True, verbose_name="Возраст ребенка")
    message = models.TextField(blank=True, verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработано")
    
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.phone}"