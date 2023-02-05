from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.home, name='home'),
    path('', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('reset/<str:pk>', views.password_reset, name='password_reset'),
]