from django.urls import path
from . import views

urlpatterns = [
    path('department/',views.department, name='department'),
    path('department/<str:ref>/',views.manage_department, name='manage_department'),
    path('manage/department/', views.unit_dept, name='unit_dept'),
    path('faculty/',views.faculty, name='faculty'),
    path('faculty/<str:ref>/',views.manage_faculty, name='manage_faculty'),
    path('manage/faculty/', views.unit_faculty, name='unit_faculty'),
]