from django.urls import path
from . import views

urlpatterns = [
    path('',views.courses, name='course_registration'),
    path('registration/initialize/', views.initialize_registration, name='initialize_registration'),
    path('applied/registration/<str:course>/', views.register_course, name='add_course'),
    path('remove/registration/<str:course>/', views.remove_course, name='remove_course'),
    path('printout/', views.print_courses, name='print_courses'),
    path('modify/', views.add_delete, name='modify'),
    path('error/', views.error, name='error'),
    path('setup', views.setup_course, name='course_setup'),
    path('query', views.query, name='query'),
    path('manage/course/<str:dept>/<str:sem>/<str:level>/', views.manage_course, name='manage_course'),
    path('query_department', views.dept_query, name='dept_query'),
    path('manage/department/<str:dept>/<str:sem>/<str:level>/', views.manage_dept, name='manage_dept'),
    path('limit', views.reg_limit, name='limit'),
    # path('lock/', views.lock_course, nmae='lock'),
]