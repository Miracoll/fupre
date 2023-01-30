from django.shortcuts import redirect, render
from django.contrib import messages
from configuration.models import User, Department, Faculty
from student.models import Student

# Create your views here.

def defer(request):
    student = User.objects.filter(username=request.user.username)
    if request.method == 'POST':
        student.update(defer=True)
        messages.success(request, 'Deferment activated successfully')
        return redirect('home')
    return render(request, 'programme/defer.html')

def resume(request):
    student = User.objects.filter(username=request.user.username)
    if request.method == 'POST':
        student.update(defer=False)
        messages.success(request, 'Deferment deactivated successfully')
        return redirect('home')
    return render(request, 'programme/resume.html')

def change(request):
    user = User.objects.get(username=request.user.username)
    student = Student.objects.get(registration_num=user)
    dept = Department.objects.filter(faculty_id=student.faculty.id)
    context = {'dept':dept}
    return render(request, 'programme/change.html',context)