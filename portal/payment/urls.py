from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_payment, name='payment'),
    path('generate/invoice/<str:reference>/', views.generate_invoice, name='generate_invoice'),
    path('history/', views.payment_history, name='history'),
]