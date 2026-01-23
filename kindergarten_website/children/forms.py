# children/forms.py
from django import forms
from .models import Child

class SimpleChildForm(forms.ModelForm):
    """Упрощенная форма ребенка для регистрации (только имя и дата рождения)"""
    class Meta:
        model = Child
        fields = ['first_name', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'Дата рождения ребенка'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя ребенка'
            }),
        }
        labels = {
            'first_name': 'Имя ребенка',
            'birth_date': 'Дата рождения',
        }

class ChildForm(forms.ModelForm):
    """Полная форма для добавления/редактирования ребенка"""
    class Meta:
        model = Child
        fields = ['first_name', 'last_name', 'birth_date', 'group', 
                 'photo', 'allergies', 'medical_notes']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.TextInput(attrs={'class': 'form-control'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }