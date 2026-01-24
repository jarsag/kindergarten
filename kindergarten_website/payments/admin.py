from django.contrib import admin
from .models import Invoice, Payment

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'child', 'amount', 'issue_date', 'due_date', 'status', 'payment_date')
    list_filter = ('status', 'issue_date', 'due_date', 'child__group')
    search_fields = ('invoice_number', 'child__first_name', 'child__last_name', 'description')
    readonly_fields = ('invoice_number',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('child', 'invoice_number', 'issue_date', 'due_date')
        }),
        ('Финансовая информация', {
            'fields': ('amount', 'description', 'status')
        }),
        ('Информация об оплате', {
            'fields': ('payment_date', 'payment_method', 'transaction_id'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Автоматически генерируем номер счета при создании"""
        if not obj.invoice_number:
            from datetime import datetime
            import random
            obj.invoice_number = f"INV-{datetime.now().year}-{random.randint(1000, 9999)}"
        super().save_model(request, obj, form, change)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'parent', 'amount', 'payment_date', 'status')
    list_filter = ('status', 'payment_date', 'payment_method')
    search_fields = ('transaction_id', 'parent__email', 'invoice__invoice_number')
    readonly_fields = ('payment_date',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('parent', 'invoice', 'amount')
        }),
        ('Информация об оплате', {
            'fields': ('payment_method', 'transaction_id', 'status', 'payment_date')
        }),
    )