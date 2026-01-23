from django.db import models
from children.models import Child

class DiaryEntry(models.Model):
    """Запись в электронном дневнике"""
    child = models.ForeignKey(Child, on_delete=models.CASCADE, 
                             related_name='diary_entries', verbose_name="Ребенок")
    date = models.DateField(verbose_name="Дата", auto_now_add=True)
    
    # Настроение и состояние
    MOOD_CHOICES = [
        ('excellent', 'Отличное'),
        ('good', 'Хорошее'),
        ('normal', 'Обычное'),
        ('bad', 'Плохое'),
        ('sick', 'Болеет'),
    ]
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, 
                           verbose_name="Настроение/Состояние")
    
    # Активности
    ate_well = models.BooleanField(default=True, verbose_name="Хорошо покушал")
    slept_well = models.BooleanField(default=True, verbose_name="Хорошо спал")
    participated = models.BooleanField(default=True, verbose_name="Активно участвовал")
    
    # Заметки
    activities = models.TextField(verbose_name="Чем занимался", blank=True)
    achievements = models.TextField(verbose_name="Достижения", blank=True)
    recommendations = models.TextField(verbose_name="Рекомендации родителям", blank=True)
    teacher_notes = models.TextField(verbose_name="Заметки воспитателя", blank=True)
    
    # Медицинские наблюдения
    temperature = models.DecimalField(max_digits=3, decimal_places=1, null=True, 
                                     blank=True, verbose_name="Температура")
    medicine_taken = models.TextField(blank=True, verbose_name="Принятые лекарства")
    
    class Meta:
        verbose_name = "Запись в дневнике"
        verbose_name_plural = "Записи в дневнике"
        ordering = ['-date']
    
    def __str__(self):
        return f"Дневник {self.child.first_name} - {self.date}"