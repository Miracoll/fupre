from django.urls import path
from . import views

urlpatterns = [
    path('query',views.query, name='student_query'),
    path('manage/<str:ref>', views.manage_student, name='manage_student'),
    path('lock',views.lock, name='lock'),
    path('student/reset', views.student_reset, name='student_reset'),
]