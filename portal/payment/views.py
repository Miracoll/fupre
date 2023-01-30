from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from .models import Payment, Payment_setup
from configuration.models import User, Semester, Session
from student.models import Student
from ast import literal_eval
import requests
import secrets
import json
import hashlib

# Create your views here.

def start_payment(request):
    all_payment = Payment_setup.objects.all()
    if request.method == 'POST':
        payment_get = request.POST.get('payment')
        if not Payment_setup.objects.filter(ref=payment_get).exists():
            User.objects.filter(username=request.user.username).update(is_active=False, lock_reason='Modified value from browser')
            messages.error(request, 'Self destruction activated')
            return redirect('logout')

        url = 'https://remitademo.net/remita/exapp/api/v1/send/api/echannelsvc/merchant/api/paymentinit'
        orderid = secrets.token_hex(16)
        student = Student.objects.get(registration_num=request.user.username)
        payment = Payment_setup.objects.get(ref=payment_get)
        semester = Semester.objects.get(status=True)
        session = Session.objects.get(active=True)
        if Payment.objects.filter(student=student,semester=semester,session=session,payment=payment).exists():
            getpayment = Payment.objects.get(student=student,semester=semester,session=session,payment=payment).ref
            return redirect('generate_invoice', getpayment)
        payload = json.dumps({
            "serviceTypeId":'4430731',
            "amount":f'{payment.amount}',
            "orderId":f'{orderid}',
            "payerName":f'{student.last_name} {student.first_name} {student.other_name}',
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
        # print(dir(response))
        print(response.status_code)
        if response.status_code != '025':
            messages.error(request, 'Unable to generate RRR, pls check back later')
            return redirect('payment')
        data = response.text[7:-1]
        result = literal_eval(data)
        Payment.objects.create(
            student=student,rrr=result.get('RRR'),payment=payment,order_id=orderid,semester=semester,
            session=session,category=payment.category
        )
        getpayment = Payment.objects.get(
            student=student,rrr=result.get('RRR'),payment=payment,order_id=orderid,semester=semester,
            session=session
        ).ref
        return redirect('generate_invoice', getpayment)
    context = {'payment':all_payment}
    return render(request, 'payment/start_payment.html', context)

def generate_invoice(request, reference):
    payment = Payment.objects.get(ref=reference)
    context = {'payment':payment}
    return render(request, 'payment/invoice.html', context)

def generate_receipt(request, reference):
    payment = Payment.objects.filter(ref=reference)
    if not payment.status:
        return redirect('generate_invoice', payment.ref)
    context = {'payment':payment}
    return render(request, 'payment/receipt.html', context)

def payment_history(request):
    student = Student.objects.get(registration_num=request.user.username)
    payment = Payment.objects.filter(student_id=student.id)
    context = {'payment':payment}
    return render(request, 'payment/history.html', context)

def verify_payment(request, reference):
    payment = Payment.objects.get(order_id=reference)
    input = str(reference)+ '1946'+ '2547916'
    hash = hashlib.sha512(str(input).encode("utf-8")).hexdigest()
    url = f'https://remitademo.net/remita/exapp/api/v1/send/api/echannelsvc/2547916/{reference}/{hash}/orderstatus.reg'

    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'remitaConsumerKey=2547916,remitaConsumerToken={hash}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.status_code)
    if response.status_code != '00':
        messages.error(request, 'Unable to verify payment, pls check back later')
    else:
        print(response.text)
        # payment.update(status=1,date_paid=)
    return redirect('history')