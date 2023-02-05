from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from configuration.models import User
from .models import Student

# Create your views here.

def query(request):
    if request.method == 'POST':
        get_reg = request.POST.get('reg')
        reg = Student.objects.get(registration_num=get_reg).ref
        return redirect('manage_student',reg)
    return render(request, 'student/query.html')

def manage_student(request, ref):
    student = Student.objects.get(ref=ref)
    if request.method == 'POST':
        pass
    context = {'student':student}
    return render(request,'student/manage_student.html',context)

def lock(request):
    if 'lock' in request.POST:
        reg = request.POST.get('reg')
        reason = request.POST.get('reason')
        User.objects.filter(username=reg).update(is_active=False,lock_reason=reason)
        messages.success(request, 'Lock')
        return redirect('lock')
    if 'unlock' in request.POST:
        reg = request.POST.get('reg')
        User.objects.filter(username=reg).update(is_active=True,lock_reason='')
        messages.success(request, 'Unlock')
        return redirect('lock')
    return render(request,'student/lock.html')

def student_reset(request):
    if request.method == 'POST':
        student = request.POST.get('reg')
        if User.objects.filter(username=student).exists():
            User.objects.filter(username=student).update(password_reset=False)
            messages.success(request,'Done')
        else:
            messages.error(request,'Incorrect registration number')
        return redirect('student_reset')
    return render(request,'student/student_reset.html')