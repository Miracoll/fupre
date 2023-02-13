from django.urls import path
from . import views

urlpatterns = [
    path('logout/',views.logoutuser, name='applicant_logout'),
    path('login/',views.applicant_login, name='applicant_login'),
    path('register/',views.applicant_register, name='applicant_register'),
    path('verification/<str:uidb64>/<str:token>/',views.verification, name='verification'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('payment/',views.application_fee,name='application_payment'),
    path('check-level/',views.check_reg,name='checkreg'),
    path('personal/',views.level1,name='level1'),
    path('department/',views.level2,name='level2'),
    path('next-of-kin/',views.level3,name='level3'),
    path('olevel/',views.level4,name='level4'),
    path('printout/',views.reg_printout,name='reg_printout'),
    path('generate/invoice/',views.generate_payment,name='generate'),
    path('payment/successfull/<str:reference>/',views.successful_payment,name='successful_payment'),
    path('payment/receipt/<str:reference>/',views.receipt,name='applicant_receipt'),
]