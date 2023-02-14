from django.urls import path
from . import views

urlpatterns = [
    path('logout/',views.logoutuser, name='applicant_logout'),
    path('',views.applicant_login, name='applicant_login'),
    path('register/',views.applicant_register, name='applicant_register'),
    path('verification/<str:uidb64>/<str:token>/',views.verification, name='verification'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('payment/',views.application_fee,name='application_payment'),
    path('registration/',views.check_reg,name='checkreg'),
    path('personal/',views.level1,name='level1'),
    path('department/',views.level2,name='level2'),
    path('next-of-kin/',views.level3,name='level3'),
    path('olevel/',views.level4,name='level4'),
    path('printout/',views.reg_printout,name='reg_printout'),
    path('generate/invoice/',views.generate_payment,name='generate'),
    path('payment/successfull/<str:reference>/',views.successful_payment,name='successful_payment'),
    path('payment/receipt/<str:reference>/',views.receipt,name='applicant_receipt'),
    path('unlock/',views.unlock_form,name='unlock'),
    path('admit/',views.get_admit,name='get_admit'),
    path('admission/<str:pk>/',views.admit_applicant,name='admission'),
    path('status/',views.admission_status,name='status'),
    path('acceptance-fee/',views.acceptace_fee,name='accept'),
    path('acceptance/success/<str:reference>',views.acceptance_success,name='accept_success'),
    path('acceptance-fee/receipt/<str:pk>/',views.acceptance_receipt,name='acceptance_receipt'),
    path('upload-document/',views.upload_document,name='upload'),
    path('generate/matric-number/',views.generate_reg,name='reg_number'),
]