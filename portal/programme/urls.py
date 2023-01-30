from django.urls import path
from . import views

urlpatterns = [
    path('defer/', views.defer, name='defer'),
    path('resume/', views.resume, name='resume'),
    path('change/', views.change, name='change'),
]