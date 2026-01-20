from django.db import models

class Group(models.Model):
    AGE_CHOICES = [
        ('1.5-3', '1.5-3 года (Ясельная)'),
        ('3-4', '3-4 года (Младшая)'),
        ('4-5', '4-5 лет (Средняя)'),
        ('5-6', '5-6 лет (Старшая)'),
        ('6-7', '6-7 лет (Подготовительная)'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название группы")
    age_range = models.CharField(max_length=20, choices=AGE_CHOICES, verbose_name="Возраст")
    description = models.TextField(verbose_name="Описание")
    teacher = models.CharField(max_length=100, verbose_name="Воспитатель")
    teacher_photo = models.ImageField(upload_to='teachers/', blank=True, verbose_name="Фото воспитателя")
    group_photo = models.ImageField(upload_to='groups/', blank=True, verbose_name="Фото группы")
    capacity = models.IntegerField(default=15, verbose_name="Вместимость")
    occupied = models.IntegerField(default=0, verbose_name="Заполнено")
    
    # Общие фичи
    has_creative = models.BooleanField(default=True, verbose_name="Творческие занятия")
    has_sports = models.BooleanField(default=True, verbose_name="Спортивные занятия")
    has_music = models.BooleanField(default=True, verbose_name="Музыкальные занятия")
    has_pool = models.BooleanField(default=False, verbose_name="Бассейн")
    
    schedule = models.TextField(verbose_name="Расписание дня", blank=True)
    
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
    
    def __str__(self):
        return f"{self.name} ({self.get_age_range_display()})"
    
    def free_places(self):
        return self.capacity - self.occupied
    
    def get_age_specific_features(self):
        """Возвращает фичи, специфичные для возраста группы"""
        features = []
        
        if self.age_range == '1.5-3':
            features = [
                "Адаптация к садику",
                "Развитие мелкой моторики",
                "Первые слова и фразы",
                "Сенсорные игры",
                "Приучение к режиму дня"
            ]
        elif self.age_range == '3-4':
            features = [
                "Развитие речи",
                "Сюжетно-ролевые игры",
                "Основы самообслуживания",
                "Лепка и рисование",
                "Музыкальные занятия"
            ]
        elif self.age_range == '4-5':
            features = [
                "Подготовка к письму",
                "Логические игры",
                "Основы математики",
                "Творческие мастерские",
                "Экологическое воспитание"
            ]
        elif self.age_range == '5-6':
            features = [
                "Обучение чтению",
                "Развитие логики",
                "Английский язык (в игровой форме)",
                "Эксперименты и опыты",
                "Театральная студия"
            ]
        elif self.age_range == '6-7':
            features = [
                "Интенсивная подготовка к школе",
                "Основы грамоты и счёта",
                "Развитие памяти и внимания",
                "Проектная деятельность",
                "Психологическая готовность к школе"
            ]
        
        return features
    
    def get_general_features(self):
        """Общие фичи для всех групп"""
        return [
            "Забота и безопасность",
            "Прогулки на свежем воздухе",
            "Социализация и общение",
            "Праздники и утренники",
            "Медицинское сопровождение"
        ]