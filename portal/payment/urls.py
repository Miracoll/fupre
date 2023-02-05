from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_payment, name='payment'),
    path('generate/invoice/<str:reference>/', views.generate_invoice, name='generate_invoice'),
    path('print/receipt/<str:reference>/', views.generate_receipt, name='generate_receipt'),
    path('history/', views.payment_history, name='history'),
    path('verify/<str:reference>/', views.verify_payment, name='verify_payment'),
    path('success/<str:reference>/', views.success_payment, name='success'),
    path('error/<str:reference>', views.error_payment, name='error'),
    path('setup', views.payment_setup, name='setup'),
    path('list', views.payment_list, name='payment_list'),
    path('manage/<str:ref>', views.manage_payment, name='manage_payment'),
]