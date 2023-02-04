from django.urls import path
from . import views

urlpatterns = [
    path('',views.courses, name='course_registration'),
    path('registration/initialize/', views.initialize_registration, name='initialize_registration'),
    path('applied/registration/<str:course>/', views.register_course, name='add_course'),
    path('remove/registration/<str:course>/', views.remove_course, name='remove_course'),
    path('printout/', views.print_courses, name='print_courses'),
    path('add-delete-course/', views.requestadd, name='requestadd'),
]