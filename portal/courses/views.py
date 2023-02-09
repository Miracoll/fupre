from ast import Pass
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from datetime import datetime
from configuration.views import department
from dashboard.decorators import allowed_users
from .models import Courses, Department_setup, Registered, Donecourse
from student.models import Student
from configuration.models import Config, Department, Semester, Session, User
from payment.models import Payment
from datetime import date
from functions.functions import str2date
import csv
from io import StringIO

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def courses(request):
    user = request.user
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    student = Student.objects.get(registration_num=user.username)
    check_done = Donecourse.objects.filter(student=student,session=session,semester=semester).exists()
    context = {
        'check':check_done
    }
    return render(request, 'courses/course.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def initialize_registration(request):
    get_current = f'{date.today()}'
    current = str2date(get_current)
    get_course_date = Config.objects.get(id=1)
    course_date = str2date(f'{get_course_date.course_end_date}')
    user = request.user
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    student = Student.objects.get(registration_num=user.username)
    try:
        Payment.objects.get(student=student,session=session,complete=True,status=True)
    except Payment.DoesNotExist:
        messages.error(request, 'No tuition fee payment found')
        return redirect('payment')
    if Donecourse.objects.filter(student=student,session=session,semester=semester,status=True).exists():
        return redirect('print_courses')
    if course_date < current:
        messages.error(request,'Registration has ended for this semester, You have to pay for late registration fee')
        return redirect('payment')
    course_setup = Department_setup.objects.get(
        dept=student.dept, level=student.level, semester=semester
    )
    course_box = Courses.objects.filter(level=student.level, semester=semester.semester, dept=student.dept, active=True)
    check_done = Donecourse.objects.filter(student=student,session=session,semester=semester).exists()
    if not check_done:
        for i in course_box.values():
            course_box_unit = Courses.objects.get(
                level=i.get('level'), active=True, course_code = i.get('course_code'), course_title=i.get('course_title'),
                semester = semester.semester, dept = Department.objects.get(id=i.get('dept_id'))
            )
            if Registered.objects.filter(student=user.username, course = course_box_unit).exists():
                continue
            else:
                Registered.objects.create(student=user.username, course=course_box_unit, semester_registered=semester, session_registered=session)
        Donecourse.objects.create(student=student,session=session,semester=semester,level=student.level)
    courses = Registered.objects.filter(student=user.username, semester_registered=semester, session_registered=session)
    loaded_unit = Registered.objects.filter(
        student=user.username, semester_registered=semester, session_registered=session, lock=True
    ).aggregate(Sum('credit_unit'))
    if request.method == 'POST':
        now = datetime.now()
        Donecourse.objects.filter(student=student,session=session,semester=semester).update(status=True,registered_on=now)
        return redirect('print_courses')
    context = {
        'courses':courses,
        'student':student,
        'setup':course_setup,
        'unit':loaded_unit,
    }
    return render(request, 'courses/register.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def register_course(request, course):
    user = request.user
    student = Student.objects.get(registration_num=user.username)
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    loaded_unit = Registered.objects.filter(
        student=user.username, semester_registered=semester, session_registered=session, lock=True
    ).aggregate(Sum('credit_unit'))
    max_unit = Department_setup.objects.get(dept=student.dept, level=student.level, semester=semester).max_credit_unit
    try:
        register = Registered.objects.get(ref=course)
    except Registered.DoesNotExist:
        User.objects.filter(username=request.user.username).update(is_active=False, lock_reason='Modifying code url from browser')
        messages.error(request, 'Self destruction activated')
        return redirect('logout')
    if loaded_unit['credit_unit__sum'] == None:
        Registered.objects.filter(student=user.username, session_registered=session, semester_registered=semester, ref=course).update(lock=True)
    else:
        if loaded_unit['credit_unit__sum'] < max_unit and (loaded_unit['credit_unit__sum'] + register.credit_unit) <= max_unit:
            Registered.objects.filter(student=user.username, session_registered=session, semester_registered=semester, ref=course).update(lock=True)
        else:
            messages.warning(request, 'No space for to add current course')
    return redirect('initialize_registration')

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def remove_course(request, course):
    user = request.user
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    try:
        Registered.objects.get(ref=course)
    except Registered.DoesNotExist:
        User.objects.filter(username=request.user.username).update(is_active=False, lock_reason='Modifying code url from browser')
        messages.error(request, 'Self destruction activated')
        return redirect('logout')
    Registered.objects.filter(student=user.username, session_registered=session, semester_registered=semester, ref=course).update(lock=False)
    return redirect('initialize_registration')

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def print_courses(request):
    user = request.user
    student = Student.objects.get(registration_num=user.username)
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    try:
        Donecourse.objects.get(student=student,session=session,semester=semester,status=True)
    except Donecourse.DoesNotExist:
        return redirect('error')
    loaded_unit = Registered.objects.filter(
        student=user.username, semester_registered=semester, session_registered=session, lock=True
    ).aggregate(Sum('credit_unit'))
    course_setup = Department_setup.objects.get(dept=student.dept, level=student.level, semester=semester)
    courses = Registered.objects.filter(student=user.username, semester_registered=semester, session_registered=session, lock=True)
    context = {
        'courses':courses,
        'student':student,
        'setup':course_setup,
        'unit':loaded_unit
    }
    return render(request, 'courses/registered_courses.html', context)

# def lock_course(request):
#     now = datetime.now()
#     semester = Semester.objects.get(status=True)
#     session = Session.objects.get(active=True)
#     student = Student.objects.get(username=request.user.username)
#     Donecourse.objects.filter(student=student,session=session,semester=semester,status=True,printed_on=now)
#     return redirect('print_courses')

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def error(request):
    return render(request, 'courses/error.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def add_delete(request):
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    student = Student.objects.get(registration_num=request.user.username)
    get_current = f'{date.today()}'
    current = str2date(get_current)
    get_course_date = Config.objects.get(id=1)
    course_date = str2date(f'{get_course_date.course_end_date}')
    if request.method == 'POST':
        if Donecourse.objects.get(student=student,session=session,semester=semester).status and course_date < current:
            messages.error(request,'Registration has ended for this semester, You have to pay for late registration fee')
            return redirect('modify')
        elif not Donecourse.objects.get(student=student,session=session,semester=semester).status and course_date < current:
            messages.error(request,'Registration has ended for this semester, You have to pay for late registration fee')
            return redirect('modify')
        Donecourse.objects.filter(student=student,session=session,semester=semester).update(status=False)
        messages.success(request, 'Request granted')
        return redirect('initialize_registration')
    return render(request, 'courses/add_delete.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def setup_course(request):
    dept = Department.objects.all()
    semester = Semester.objects.all()
    if 'manual' in request.POST:
        course_title = request.POST.get('title').upper()
        course_code = request.POST.get('code').upper()
        unit = request.POST.get('unit')
        get_dept = request.POST.get('dept')
        sem = request.POST.get('semester')
        level = request.POST.get('level')
        coordinator = request.POST.get('coordinator').upper()
        core = int(request.POST.get('core'))

        department = Department.objects.get(ref=get_dept)
        new_code = course_code.replace(' ','')

        if Courses.objects.filter(course_title=new_code,dept=department).exists():
            messages.error(request, 'Course already exist')
        else:
            Courses.objects.create(course_code=new_code,course_title=course_title,credit_unit=unit,
                semester=sem,level=level,coodinator=coordinator,dept=department,core_course=bool(core)
            )
            messages.success(request, 'Course added successfully')
        return redirect('course_setup')

    if 'upload' in request.POST:
        csv_file = request.FILES["file"]
        if not csv_file.name.endswith('.csv'):
            messages.warning(request,'File is not CSV type')
            return redirect('course_setup')
        file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(StringIO(file), delimiter=',')
        next(csv_data)
        for line in csv_data:
            pass

    context = {'dept':dept, 'semester':semester}
    return render(request, 'courses/setup.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def query(request):
    dept = Department.objects.all()
    semester = Semester.objects.all()
    if request.method == 'POST':
        department = request.POST.get('dept')
        sem = request.POST.get('semester')
        level = request.POST.get('level')
        return redirect('manage_course',department,sem,level)
    context = {'dept':dept, 'semester':semester}
    return render(request, 'courses/query.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def manage_course(request, dept, sem, level):
    department = Department.objects.get(ref=dept)
    semester = Semester.objects.get(ref=sem)
    courses = Courses.objects.filter(dept=department,semester=str(semester.semester),level=level)
    context = {'course':courses}
    return render(request, 'courses/manage_course.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_course(request, reference):
    dept = Department.objects.all()
    semester = Semester.objects.all()
    courses = Courses.objects.get(ref=reference)
    if request.method == 'POST':
        course_title = request.POST.get('title').upper()
        course_code = request.POST.get('code').upper()
        unit = request.POST.get('unit')
        get_dept = request.POST.get('dept')
        sem = request.POST.get('semester')
        level = request.POST.get('level')
        coordinator = request.POST.get('coordinator').upper()
        core = int(request.POST.get('core'))

        department = Department.objects.get(ref=get_dept)
        new_code = course_code.replace(' ','')

        Courses.objects.filter.update(
            course_code=new_code,course_title=course_title,credit_unit=unit,
            semester=sem,level=level,coodinator=coordinator,dept=department,core_course=bool(core)
        )
    context = {'course':courses,'dept':dept,'semester':semester}
    return render(request, 'courses/update_course.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def dept_query(request):
    dept = Department.objects.all()
    semester = Semester.objects.all()
    if request.method == 'POST':
        department = request.POST.get('dept')
        sem = request.POST.get('semester')
        level = request.POST.get('level')
        return redirect('manage_dept',department,sem,level)
    context = {'dept':dept, 'semester':semester}
    return render(request, 'courses/query_dept.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def manage_dept(request, dept, sem, level):
    department = Department.objects.get(ref=dept)
    semester = Semester.objects.get(ref=sem)
    try:
        dept_setup = Department_setup.objects.get(dept=department,semester=str(semester.semester),level=level)
    except Department_setup.DoesNotExist:
        messages.error(request, 'No result from query')
        return redirect('dept_query')
    if request.method == 'POST':
        max_credit_unit = request.POST.get('maxx')
        Department_setup.objects.filter(dept=department,semester=str(semester.semester),level=level).update(
            max_credit_unit=int(max_credit_unit)
        )
        messages.success(request, 'successful')
        return redirect('manage_dept',dept,sem,level)
    context = {'course':dept_setup}
    return render(request, 'courses/manage_dept.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def reg_limit(request):
    if request.method == 'POST':
        get_start = request.POST.get('start')
        get_end = request.POST.get('end')
        start = str2date(get_start)
        end = str2date(get_end)
        if end < start:
            messages.error(request, 'Start date should not be greater than end date')
            return redirect('limit')
        Config.objects.filter(id=1).update(course_start_date=start,course_end_date=end,course_reg_status=True)
        messages.success(request,'Successful')
        return redirect('limit')
    return render(request, 'courses/limit.html')