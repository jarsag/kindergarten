from django.db import models
from accounts.models import CustomUser

class Child(models.Model):
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                               related_name='children', verbose_name="Родитель")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")
    group = models.CharField(max_length=100, verbose_name="Группа", blank=True)
    photo = models.ImageField(upload_to='children_photos/', 
                              blank=True, null=True, verbose_name="Фотография")
    allergies = models.TextField(blank=True, verbose_name="Аллергии/Особенности")
    medical_notes = models.TextField(blank=True, verbose_name="Медицинские заметки")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def age(self):
        """Вычисляет возраст ребенка"""
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    class Meta:
        verbose_name = "Ребенок"
        verbose_name_plural = "Дети"