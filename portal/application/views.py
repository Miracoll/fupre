from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from dashboard.decorators import allowed_users
from .models import Applicant, Course, Personal,NOK,Olevel
from .models import Payment as AP
from .models import Student as AS
from .forms import Level1Form, NOKForm
from payment.models import Payment,Payment_setup
from utils import token_generator
from configuration.models import Config, Department,User,Role,Session
import secrets
import json
import hashlib
import requests
from ast import literal_eval
from datetime import datetime

# Create your views here.

def applicant_login(request):
    sch_name = Config.objects.get(id=1).school_name
    if request.method == 'POST':
        username = request.POST.get('reg')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.warning(request,'applicant does not exist')
            return redirect('applicant_login')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('generate')
        else:
            messages.warning(request,'username/password is incorrect')
            return redirect('applicant_login')
    context = {'name':sch_name}
    return render(request,'application/login.html',context)

def applicant_register(request):
    if request.method == 'POST':
        session = Session.objects.get(active=True).session
        last_name = request.POST.get('last-name')
        first_name = request.POST.get('first-name')
        other_name = request.POST.get('other-name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('psw')
        jamb = request.POST.get('jamb')

        if User.objects.filter(email=email).exists() or User.objects.filter(username=jamb).exists():
            messages.error(request, 'Email or jamb registration number already used')
            return redirect('applicant_register')

        Applicant.objects.create(
            last_name=last_name,first_name=first_name,other_name=other_name,mobile=mobile,email=email,jamb=jamb,
            session=session
        )

        user = User.objects.create_user(jamb,email,password)
        user.is_staff = True
        user.is_superuser = False
        user.last_name = last_name
        user.first_name = first_name
        user.is_active = True
        user.save()

        # # Verify email
        # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        # token = token_generator.make_token(user)
        # domain = get_current_site(request).domain
        # relative = reverse('verification',kwargs={'uidb64':uidb64,'token':token})
        # activate_url = 'http//'+domain+relative
        
        # subject = 'FUPRE EMAIL VERIFICATION'
        # recipient = [email]
        # text_content = f"Hello {last_name} {first_name} please use this link to verify your account\n {activate_url}"
        # html_content = f"<div><p>Hello {last_name} {first_name} please use this link to verify your account\n {activate_url}</p></div>"
        # message = EmailMultiAlternatives(subject=subject, body=text_content, to=recipient)
        # message.attach_alternative(html_content, 'text/html')
        # message.send()

        role = Role.objects.filter(keyword = 'applicant')
        if len(role) == 0:
            Group.objects.create(name='applicant')

        User.objects.filter(username = jamb).update(image = 'passport.jpg')
            
        userid = User.objects.get(username=jamb).id
        getgroup = Group.objects.get(name='applicant')
        getgroup.user_set.add(userid)

        messages.success(request, 'Registration successful')
        return redirect('applicant_login')

    return render(request,'application/register.html')

def verification(request, uidb64, token):
    return redirect('applicant_login')

@login_required(login_url='applicant_login')
@allowed_users(allowed_roles=['applicant'])
def generate_payment(request):
    session = Session.objects.get(active=True).session
    user = request.user
    url = 'https://remitademo.net/remita/exapp/api/v1/send/api/echannelsvc/merchant/api/paymentinit'
    orderid = secrets.token_hex(16)
    student = Applicant.objects.get(jamb=user.username)
    payment = Payment_setup.objects.get(category='application')
    if AP.objects.filter(applicant=student,session=session,payment=payment,status=True).exists():
        getpayment = AP.objects.get(applicant=student,session=session,payment=payment).ref
        return redirect('dashboard')
    
    if not AP.objects.filter(applicant=student,session=session,payment=payment).exists():
        payload = json.dumps({
            "serviceTypeId":'4430731',
            "amount":f'{payment.amount}',
            "orderId":f'{orderid}',
            "payerName":f'{student.last_name} {student.first_name}',
            "payerEmail":f'{student.email}',
            "payerPhone":f'{student.mobile}',
            "description":f'Payment for {payment.payment_type}'
        })
        input = '2547916' + '4430731' + str(orderid)+ str(payment.amount) + '1946'
        hash = hashlib.sha512(str(input).encode("utf-8")).hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'remitaConsumerKey=2547916,remitaConsumerToken={hash}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        
        if str(response.status_code) != '200':
            messages.error(request, 'Unable to generate RRR, pls check back later')
            return redirect('payment')
        data = response.text[7:-1]
        result = literal_eval(data)
        AP.objects.create(
            applicant=student,rrr=result.get('RRR'),session=session,payment=payment,order_id=orderid,category=payment.category,
            amount=payment.amount
        )
    getpayment = AP.objects.get(
        applicant=student,session=session,payment=payment
    )
    # return redirect('application_payment', getpayment)
    
    context = {'payment':getpayment}
    return render(request,'application/application_fee.html',context)

@login_required(login_url='applicant_login')
@allowed_users(allowed_roles=['applicant'])
def dashboard(request):
    return render(request,'application/dashboard.html')

@login_required(login_url='applicant_login')
@allowed_users(allowed_roles=['applicant'])
def application_fee(request, reference):
    payment = AP.objects.get(ref=reference)
    if payment.status:
        return redirect('checkreg')
    context = {'payment':payment}
    return render(request,'application/application_fee.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def check_reg(request):
    session = Session.objects.get(active=True).session
    user = request.user
    applicant = Applicant.objects.get(jamb=user.username)
    get_level = AS.objects.get(applicant=applicant,session=session).level
    if get_level == 1:
        return redirect('level1')
    elif get_level == 2:
        return redirect('level2')
    elif get_level == 3:
        return redirect('level3')
    elif get_level == 4:
        return redirect('level4')
    elif get_level == 5:
        return redirect('reg_printout')

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def successful_payment(request, reference):
    session = Session.objects.get(active=True).session
    now = datetime.now()
    AP.objects.filter(ref=reference).update(status=True,paid_on=now)
    user = request.user
    applicant = Applicant.objects.get(jamb=user.username)
    Personal.objects.create(
        last_name=applicant.last_name,first_name=applicant.first_name,other_name=applicant.other_name,email=applicant.email,
        mobile=applicant.mobile,jamb=applicant.jamb,applicant=applicant,session=session
    )
    if not AS.objects.filter(applicant=applicant,session=session).exists():
        AS.objects.create(applicant=applicant,session=session,level=1)
    messages.success(request, 'Payment successful')
    return redirect('level1')

@login_required(login_url='login')
@allowed_users(allowed_roles=['applicant'])
def receipt(request, reference):
    payment = AP.objects.get(ref=reference)
    context = {'payment':payment}
    return render(request,'application/receipt.html',context)

def logoutuser(request):
    logout(request)
    return redirect('applicant_login')

@login_required(login_url='applicant_login')
@allowed_users(allowed_roles=['applicant'])
def level1(request):
    session = Session.objects.get(active=True).session
    user = request.user
    applicant = Applicant.objects.get(jamb=user.username)
    person = Personal.objects.get(jamb=user.username)
    form = Level1Form(instance = person)
    
    if request.method == 'POST':
        form = Level1Form(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            AS.objects.filter(applicant=applicant,session=session).update(level=2,personal=person)
            messages.success(request, 'Saved')
            return redirect('level2')
    context = {'form':form}
    return render(request,'application/level1.html',context)

@login_required(login_url='applicant_login')
@allowed_users(allowed_roles=['applicant'])
def level2(request):
    session = Session.objects.get(active=True).session
    user = request.user
    applicant = Applicant.objects.get(jamb=user.username)
    dept = Department.objects.all()
    if request.method == 'POST':
        dept1 = request.POST.get('dept1')
        dept2 = request.POST.get('dept2')
        getdept1 = Department.objects.get(ref=dept1)
        getdept2 = Department.objects.get(ref=dept2)
        if not Course.objects.filter(applicant=applicant,session=session).exists():
            Course.objects.create(applicant=applicant,session=session,dept1=getdept1,dept2=getdept2)
            NOK.objects.create(applicant=applicant)
        else:
            Course.objects.filter(applicant=applicant,session=session).update(dept1=getdept1,dept2=getdept2)
        course = Course.objects.get(applicant=applicant,session=session)
        AS.objects.filter(applicant=applicant,session=session).update(level=3,course=course)
        messages.success(request,'Saved')
        return redirect('level3')
    context = {'dept':dept}
    return render(request,'application/level2.html',context)

@login_required(login_url='applicant_login')
@allowed_users(allowed_roles=['applicant'])
def level3(request):
    session = Session.objects.get(active=True).session
    user = request.user
    applicant = Applicant.objects.get(jamb=user.username)
    person = NOK.objects.get(applicant=applicant)
    form = NOKForm(instance = person)
    if request.method == 'POST':
        form = NOKForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            if not Olevel.objects.filter(applicant=applicant,session=session).exists():
                Olevel.objects.create(applicant=applicant,session=session)
            AS.objects.filter(applicant=applicant,session=session).update(level=4,nok=person)
            messages.success(request, 'Saved')
            return redirect('level4')
    context = {'form':form}
    return render(request,'application/level3.html',context)

@login_required(login_url='applicant_login')
@allowed_users(allowed_roles=['applicant'])
def level4(request):
    session = Session.objects.get(active=True).session
    user = request.user
    applicant = Applicant.objects.get(jamb=user.username)
    olevel = Olevel.objects.get(applicant=applicant,session=session)
    if request.method == 'POST':
        examtype = request.POST.get('examtype1')
        examyear = request.POST.get('examyear1')
        examnumber = request.POST.get('examnumber1')
        exaamcenter = request.POST.get('examcenter1')
        sub1 = request.POST.get('sub1')
        grade1 = request.POST.get('grade1')
        sub2 = request.POST.get('sub2')
        grade2 = request.POST.get('grade2')
        sub3 = request.POST.get('sub3')
        grade3 = request.POST.get('grade3')
        sub4 = request.POST.get('sub4')
        grade4 = request.POST.get('grade4')
        sub5 = request.POST.get('sub5')
        grade5 = request.POST.get('grade5')
        sub6 = request.POST.get('sub6')
        grade6 = request.POST.get('grade6')
        sub7 = request.POST.get('sub7')
        grade7 = request.POST.get('grade7')
        sub8 = request.POST.get('sub8')
        grade8 = request.POST.get('grade8')
        sub9 = request.POST.get('sub9')
        grade9 = request.POST.get('grade9')
        
        examtype2 = request.POST.get('examtype11')
        examyear2 = request.POST.get('examyear11')
        examnumber2 = request.POST.get('examnumber11')
        exaamcenter2 = request.POST.get('examcenter11')
        sub12 = request.POST.get('sub11')
        grade12 = request.POST.get('grade11')
        sub22 = request.POST.get('sub21')
        grade22 = request.POST.get('grade21')
        sub32 = request.POST.get('sub31')
        grade32 = request.POST.get('grade31')
        sub42 = request.POST.get('sub41')
        grade42 = request.POST.get('grade41')
        sub52 = request.POST.get('sub51')
        grade52 = request.POST.get('grade51')
        sub62 = request.POST.get('sub61')
        grade62 = request.POST.get('grade61')
        sub72 = request.POST.get('sub71')
        grade72 = request.POST.get('grade71')
        sub82 = request.POST.get('sub81')
        grade82 = request.POST.get('grade81')
        sub92 = request.POST.get('sub91')
        grade92 = request.POST.get('grade91')

        Olevel.objects.filter(applicant=applicant,session=session).update(
            exam_type=examtype,exam_number=examnumber,exam_year=examyear,exam_center=exaamcenter,sub1=sub1,grade1=grade1,
            sub2=sub2,grade2=grade2,sub3=sub3,grade3=grade3,sub4=sub4,grade4=grade4,sub5=sub5,grade5=grade5,sub6=sub6,grade6=grade6,sub7=sub7,grade7=grade7,sub8=sub8,grade8=grade8,sub9=sub9,grade9=grade9,
            exam_type2=examtype2,exam_number2=examnumber2,exam_year2=examyear2,exam_center2=exaamcenter2,sub12=sub12,grade12=grade12,sub22=sub22,grade22=grade22,
            sub32=sub32,grade32=grade32,sub42=sub42,grade42=grade42,sub52=sub52,grade52=grade52,sub62=sub62,grade62=grade62,
            sub72=sub72,grade72=grade72,sub82=sub82,grade82=grade82,sub92=sub92,grade92=grade92
        )
        AS.objects.filter(applicant=applicant,session=session).update(level=5,olevel=olevel)
        messages.success(request,'Saved')
        return redirect('reg_printout')
    context={'olevel':olevel}
    return render(request,'application/level4.html',context)

@login_required(login_url='applicant_login')
@allowed_users(allowed_roles=['applicant'])
def reg_printout(request):
    session = Session.objects.get(active=True).session
    user = request.user
    applicant = Applicant.objects.get(jamb=user.username)
    student = AS.objects.get(applicant=applicant,session=session)
    context = {'student':student}
    return render(request,'application/printout.html',context)