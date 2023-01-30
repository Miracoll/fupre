from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.viewhostel, name='viewhostel'),
    path('assign/<str:pk>/', views.assign2occupant, name='assign2occupant'),
    path('printout/<str:pk>/', views.hostelprintout, name='hostelprintout'),
]