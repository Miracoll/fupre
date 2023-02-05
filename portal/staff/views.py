from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from dashboard.decorators import allowed_users
from student.models import Student
from configuration.models import User, Role, Config

# Create your views here.

def home(request):
    return render(request, 'staff/index.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def home(request):
    user = request.user.username
    return render(request, 'staff/index.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def adminaccount(request):
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            messages.error(request, 'Email or username already used')
            return redirect('adminaccount')

        user = User.objects.create_user(username,email,password)
        user.is_staff = True
        user.is_superuser = True
        user.last_name = last_name
        user.first_name = first_name
        user.save()

        role = Role.objects.filter(keyword = 'admin')
        if len(role) == 0:
            Group.objects.create(name='admin')

        User.objects.filter(username = username).update(image = 'passport.jpg')
            
        userid = User.objects.get(username=username).id
        getgroup = Group.objects.get(name='admin')
        getgroup.user_set.add(userid)

        if len(Config.objects.all()) == 0:
            Config.objects.create(school_name = '')

        messages.success(request, 'Creation successful')
        return redirect('adminaccount')
    return render(request, 'staff/adminaccount.html')



# def loginuser(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         try:
#             user = User.objects.get(username=username)
#         except:
#             messages.warning(request,'username does not exist')
#             return redirect('login')
        
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             messages.warning(request,'Incorrect username or password')
#             return redirect('login')
#     return render(request, 'dashboard/login.html')

# def logoutuser(request):
#     logout(request)
#     return redirect('signin')