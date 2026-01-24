from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Invoice, Payment
from .forms import PaymentForm
from children.models import Child

@login_required
def payments_dashboard(request):
    """Главная страница онлайн-оплаты"""
    # Получаем детей текущего пользователя
    children = request.user.children.all()
    
    # Получаем все счета детей пользователя
    invoices = Invoice.objects.filter(child__in=children).order_by('-issue_date')
    
    # Статистика
    total_invoices = invoices.count()
    total_pending = invoices.filter(status='pending').count()
    total_paid = invoices.filter(status='paid').count()
    total_amount = invoices.aggregate(total=Sum('amount'))['total'] or 0
    
    # Просроченные счета
    overdue_invoices = []
    for invoice in invoices.filter(status='pending'):
        if invoice.is_overdue():
            overdue_invoices.append(invoice)
    
    return render(request, 'payments/dashboard.html', {
        'children': children,
        'invoices': invoices[:10],  # Последние 10 счетов
        'overdue_invoices': overdue_invoices,
        'total_invoices': total_invoices,
        'total_pending': total_pending,
        'total_paid': total_paid,
        'total_amount': total_amount,
    })

@login_required
def invoices_list(request):
    """Список всех счетов"""
    children = request.user.children.all()
    invoices = Invoice.objects.filter(child__in=children).order_by('-issue_date')
    
    # Фильтрация
    status_filter = request.GET.get('status', '')
    child_filter = request.GET.get('child', '')
    
    if status_filter:
        invoices = invoices.filter(status=status_filter)
    if child_filter:
        invoices = invoices.filter(child_id=child_filter)
    
    return render(request, 'payments/invoices_list.html', {
        'invoices': invoices,
        'children': children,
        'status_filter': status_filter,
        'child_filter': child_filter,
    })

@login_required
def invoice_detail(request, invoice_id):
    """Детальная информация о счете"""
    invoice = get_object_or_404(Invoice, id=invoice_id, child__parent=request.user)
    
    return render(request, 'payments/invoice_detail.html', {
        'invoice': invoice,
    })

@login_required
def make_payment(request, invoice_id):
    """Оплата счета"""
    invoice = get_object_or_404(Invoice, id=invoice_id, child__parent=request.user)
    
    if invoice.status == 'paid':
        messages.warning(request, 'Этот счет уже оплачен')
        return redirect('payments:invoice_detail', invoice_id=invoice_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Имитация оплаты (в реальном проекте здесь интеграция с платежной системой)
            try:
                # Обновляем счет
                invoice.status = 'paid'
                invoice.payment_date = timezone.now().date()
                invoice.payment_method = 'Банковская карта'
                invoice.transaction_id = f"TRX{int(timezone.now().timestamp())}"
                invoice.save()
                
                # Создаем запись о платеже
                Payment.objects.create(
                    parent=request.user,
                    invoice=invoice,
                    amount=invoice.amount,
                    payment_method='Банковская карта',
                    transaction_id=invoice.transaction_id,
                    status='completed'
                )
                
                messages.success(request, f'Счет #{invoice.invoice_number} успешно оплачен!')
                return redirect('payments:invoice_detail', invoice_id=invoice_id)
                
            except Exception as e:
                messages.error(request, f'Ошибка при оплате: {str(e)}')
    else:
        # Автоматически заполняем сумму
        initial_data = {'amount': invoice.amount}
        form = PaymentForm(initial=initial_data)
    
    return render(request, 'payments/make_payment.html', {
        'form': form,
        'invoice': invoice,
    })

@login_required
def payment_history(request):
    """История платежей"""
    payments = Payment.objects.filter(parent=request.user).order_by('-payment_date')
    
    return render(request, 'payments/payment_history.html', {
        'payments': payments,
    })