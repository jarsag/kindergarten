from django import forms
from .models import DiaryEntry

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['mood', 'ate_well', 'slept_well', 'participated',
                 'activities', 'achievements', 'recommendations',
                 'teacher_notes', 'temperature', 'medicine_taken']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'mood': forms.Select(attrs={'class': 'form-control'}),
            'activities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'teacher_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'medicine_taken': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'mood': 'Настроение ребенка',
            'ate_well': 'Хорошо покушал',
            'slept_well': 'Хорошо спал',
            'participated': 'Активно участвовал',
            'activities': 'Чем занимался сегодня',
            'achievements': 'Достижения и успехи',
            'recommendations': 'Рекомендации родителям',
            'teacher_notes': 'Заметки воспитателя',
            'temperature': 'Температура (°C)',
            'medicine_taken': 'Принятые лекарства',
        }