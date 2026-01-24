from django import forms

class PaymentForm(forms.Form):
    """Форма для оплаты счета"""
    card_number = forms.CharField(
        label="Номер карты",
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0000 0000 0000 0000',
            'data-mask': '0000 0000 0000 0000'
        })
    )
    
    card_expiry = forms.CharField(
        label="Срок действия",
        max_length=7,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/ГГ',
            'data-mask': '00/00'
        })
    )
    
    card_cvc = forms.CharField(
        label="CVC/CVV",
        max_length=4,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '123',
            'data-mask': '000'
        })
    )
    
    cardholder_name = forms.CharField(
        label="Имя держателя карты",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'IVAN IVANOV'
        })
    )
    
    amount = forms.DecimalField(
        label="Сумма к оплате",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        })
    )