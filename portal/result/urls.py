from django.urls import path
from . import views

urlpatterns = [
    path('checker/', views.get_result, name='get_result'),
    path('<str:isession>/<str:isemester>/', views.result, name='result'),
]