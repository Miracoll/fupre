from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Sum
from .models import Courses, Department_setup, Registered
from student.models import Student
from configuration.models import Department, Semester, Session, User

# Create your views here.

def courses(request):
    return render(request, 'courses/course.html')

def initialize_registration(request):
    user = request.user
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    student = Student.objects.get(registration_num=user.username)
    course_setup = Department_setup.objects.get(
        dept=student.dept, level=student.level, semester=semester
    )
    course_box = Courses.objects.filter(level=student.level, semester=semester.semester, dept=student.dept, active=True)
    for i in course_box.values():
        course_box_unit = Courses.objects.get(
            level=i.get('level'), active=True, course_code = i.get('course_code'), course_title=i.get('course_title'),
            semester = Semester.objects.get(id=i.get('semester_id')), dept = Department.objects.get(id=i.get('dept_id'))
        )
        if Registered.objects.filter(student=user.username, course = course_box_unit).exists():
            continue
        else:
            Registered.objects.create(student=user.username, course=course_box_unit, semester_registered=semester, session_registered=session)
    courses = Registered.objects.filter(student=user.username, semester_registered=semester, session_registered=session)
    loaded_unit = Registered.objects.filter(
        student=user.username, semester_registered=semester, session_registered=session, lock=True
    ).aggregate(Sum('credit_unit'))
    context = {
        'courses':courses,
        'student':student,
        'setup':course_setup,
        'unit':loaded_unit
    }
    return render(request, 'courses/register.html', context)

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
    if loaded_unit['credit_unit__sum'] < max_unit and (loaded_unit['credit_unit__sum'] + register.credit_unit) <= max_unit:
        Registered.objects.filter(student=user.username, session_registered=session, semester_registered=semester, ref=course).update(lock=True)
    else:
        messages.warning(request, 'No space for to add current course')
    return redirect('initialize_registration')

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

def print_courses(request):
    user = request.user
    student = Student.objects.get(registration_num=user.username)
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
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

def requestadd(request):
    return render(request, 'courses/request.html')