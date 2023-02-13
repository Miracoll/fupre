from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dashboard.decorators import allowed_users
from student.models import Student
from configuration.models import User
from configuration.models import Semester, Session

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def home(request):
    user = request.user.username
    student = Student.objects.get(registration_num=user)
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    context = {'student':student, 'semester':semester, 'session':session }
    return render(request, 'dashboard/dashboard.html', context)

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            get_user = User.objects.get(username=username)
            print(get_user)
        except:
            messages.warning(request,'username does not exist')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            login(request,user)
            if not get_user.password_reset:
                return redirect('password_reset',username)
            else:
                if get_user.groups.filter(name='admin').exists():
                    return redirect('admin_home')
                else:
                    return redirect('home')
        else:
            messages.warning(request,'Incorrect username or password')
            return redirect('login')
    return render(request, 'dashboard/login.html')

def logoutuser(request):
    logout(request)
    return redirect('login')


def password_reset(request,pk):
    if request.method == 'POST':
        getpass = User.objects.get(username=pk).password_reset
        if not getpass:
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')

            if pass1 == pass2:
                u = User.objects.get(username=pk)
                u.set_password(pass1)
                u.save()
                User.objects.filter(username=pk).update(password_reset=True)
                user = authenticate(request, username=pk, password=pass1)
                if user is not None:
                    login(request,user)
                    return redirect('home')
            else:
                messages.warning(request, 'Password did not match')
                return redirect('password_reset',pk)
    return render(request, 'dashboard/password_reset.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def profile(request):
    user = request.user.username
    student = Student.objects.get(registration_num=user)
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    context = {'student':student, 'semester':semester, 'session':session }
    return render(request, 'dashboard/profile.html', context )