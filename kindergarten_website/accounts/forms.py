# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    # Делаем username необязательным
    username = forms.CharField(
        required=False,
        label="Имя пользователя (необязательно)",
        help_text="Если не укажете, будет использован email"
    )
    
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2',
                 'first_name', 'last_name', 'phone',
                 'child_name', 'child_age', 'child_group')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        # Если username пустой, используем email
        if not user.username:
            user.username = user.email
        
        if commit:
            user.save()
        return user

# accounts/forms.py (дополнить LoginForm)
class LoginForm(forms.Form):
    """Форма входа, которая принимает email или username"""
    username = forms.CharField(
        label="Email или имя пользователя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email или имя пользователя'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        # Валидация будет в view
        return cleaned_data