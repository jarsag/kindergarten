from django.db import models
from accounts.models import CustomUser
from children.models import Child

class Invoice(models.Model):
    """Счет на оплату"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('overdue', 'Просрочен'),
        ('cancelled', 'Отменен'),
    ]
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, 
                             related_name='invoices', verbose_name="Ребенок")
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="Номер счета")
    issue_date = models.DateField(auto_now_add=True, verbose_name="Дата выставления")
    due_date = models.DateField(verbose_name="Срок оплаты")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    description = models.TextField(verbose_name="Назначение платежа")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                             default='pending', verbose_name="Статус")
    
    # Поля для оплаты
    payment_date = models.DateField(null=True, blank=True, verbose_name="Дата оплаты")
    payment_method = models.CharField(max_length=50, blank=True, verbose_name="Способ оплаты")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="ID транзакции")
    
    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Счет #{self.invoice_number} - {self.child.first_name} ({self.amount} руб.)"
    
    def is_overdue(self):
        """Проверяет, просрочен ли счет"""
        from datetime import date
        return self.status == 'pending' and self.due_date < date.today()
    
    def days_remaining(self):
        """Осталось дней до просрочки"""
        from datetime import date
        if self.due_date >= date.today():
            return (self.due_date - date.today()).days
        return 0

class Payment(models.Model):
    """История платежей"""
    parent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                              related_name='payments', verbose_name="Родитель")
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, 
                                  verbose_name="Счет")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment_method = models.CharField(max_length=50, verbose_name="Способ оплаты")
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name="ID транзакции")
    status = models.CharField(max_length=20, default='completed', verbose_name="Статус")
    
    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Платеж #{self.transaction_id} - {self.amount} руб."