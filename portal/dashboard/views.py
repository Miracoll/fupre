from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from student.models import Student
from configuration.models import User

# Create your views here.

def home(request):
    user = request.user.username
    student = Student.objects.get(registration_num=user)
    context = {'student':student}
    return render(request, 'dashboard/dashboard.html', context)

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.warning(request,'username does not exist')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request,'Incorrect username or password')
            return redirect('login')
    return render(request, 'dashboard/login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')