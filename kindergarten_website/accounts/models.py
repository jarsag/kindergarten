from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Родительская информация
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    #child_name = models.CharField(max_length=100, verbose_name="Имя ребенка", blank=True)
    #child_age = models.IntegerField(verbose_name="Возраст ребенка", null=True, blank=True)
    #child_group = models.CharField(max_length=100, verbose_name="Группа ребенка", blank=True)
    
    # Дополнительные поля
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    notification_email = models.BooleanField(default=True, verbose_name="Email уведомления")
    notification_sms = models.BooleanField(default=False, verbose_name="SMS уведомления")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"