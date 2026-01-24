from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payments_dashboard, name='dashboard'),
    path('invoices/', views.invoices_list, name='invoices_list'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/pay/', views.make_payment, name='make_payment'),
    path('history/', views.payment_history, name='payment_history'),
]