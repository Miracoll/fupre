from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dashboard.decorators import allowed_users
from .models import Certification, Department, Faculty, Semester, Session
from courses.models import Department_setup
from student.models import Student

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def department(request):
    faculty = Faculty.objects.all()
    certification = Certification.objects.all()
    if request.method == 'POST':
        get_faculty = request.POST.get('faculty')
        dept_code = request.POST.get('dept_code')
        dept_name = request.POST.get('dept').upper()
        hod = request.POST.get('hod').upper()
        level = int(request.POST.get('level'))
        cert = request.POST.get('cert')
        abbr = request.POST.get('abbr').upper()

        unit_faculty = Faculty.objects.get(name=get_faculty)

        if Department.objects.filter(faculty=unit_faculty,name=dept_name).exists():
            messages.error(request, 'Department already exist')
        else:
            Department.objects.create(code=dept_code,faculty=unit_faculty,name=dept_name,max_level=level,hod=hod,cert=cert,dept_abbr=abbr)
            messages.success(request, 'Department created')

        # Setup department for course registration
        semester = Semester.objects.values()
        dept = Department.objects.get(name=dept_name)
        iyear = int(level/100)
        for i in semester:
            sem = i.get('semester')
            for year in range(iyear):
                new_level = (int(year) + 1) * 100
                Department_setup.objects.create(dept=dept,semester=sem,level=new_level,max_credit_unit=25)

        return redirect('department')
    context = {'faculty':faculty, 'cert':certification}
    return render(request, 'configuration/department.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def unit_dept(request):
    dept = Department.objects.all()
    context = {'dept':dept}
    return render(request, 'configuration/manage.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def manage_department(request, ref):
    department = Department.objects.get(ref=ref)
    print(department)
    faculty = Faculty.objects.all()
    certification = Certification.objects.all()
    if request.method == 'POST':
        get_faculty = request.POST.get('faculty')
        dept_code = request.POST.get('dept_code')
        dept_name = request.POST.get('dept').upper()
        hod = request.POST.get('hod').upper()
        level = int(request.POST.get('level'))
        cert = request.POST.get('cert')
        year = int(level/100)

        unit_faculty = Faculty.objects.get(name=get_faculty)
        Department.objects.filter(ref=ref).update(code=dept_code,faculty=unit_faculty,name=dept_name,
            max_level=level,hod=hod,cert=cert,number_of_years=year
        )
        messages.success(request, 'Department updated')
        return redirect('manage_department', ref)
    context = {'faculty':faculty, 'cert':certification,'dept':department}
    return render(request, 'configuration/manage_dept.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def faculty(request):
    if request.method == 'POST':
        faculty = request.POST.get('fac').upper()
        fac_code = request.POST.get('fac_code')
        dean = request.POST.get('dean').upper()

        if Faculty.objects.filter(name=faculty).exists():
            messages.error(request, 'Faculty already exist')
        else:
            Faculty.objects.create(code=fac_code,name=faculty,dean=dean)
            messages.success(request, 'Faculty created')
        return redirect('faculty')
    return render(request, 'configuration/faculty.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def manage_faculty(request, ref):
    get_faculty = Faculty.objects.get(ref=ref)
    if request.method == 'POST':
        faculty = request.POST.get('fac').upper()
        fac_code = request.POST.get('fac_code')
        dean = request.POST.get('dean').upper()

        Faculty.objects.filter(ref=ref).update(code=fac_code,name=faculty,dean=dean)
        messages.success(request, 'Faculty updated')
        return redirect('manage_faculty', ref)
    context = {'faculty':get_faculty}
    return render(request, 'configuration/manage_fac.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def unit_faculty(request):
    faculty = Faculty.objects.all()
    context = {'faculty':faculty}
    return render(request, 'configuration/faculty_unit.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def setup_session(request):
    if request.method == 'POST':
        session = request.POST.get('session')
        year = request.POST.get('year')

        students = Student.objects.all()
        for i in students.values():
            student_dept = i.get('dept_id')
            max_year = Department.objects.get(id=student_dept).max_level
            student_level = i.get('level')
            if student_level >= max_year:
                continue
            else:
                student_level += 100
                Student.objects.filter(registration_num=i.get('registration_num')).update(level=student_level)
        Session.objects.filter(active=True).update(active=False)
        Session.objects.create(session=session,year=year)
        messages.success(request, 'Created successfully')
        return redirect('session')
    context = {}
    return render(request, 'configuration/setup_session.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def switch_session(request):
    get_session = Session.objects.all()
    if request.method == 'POST':
        session = request.POST.get('session')
        Session.objects.filter(active=True).update(active=False)
        Session.objects.filter(session=session).update(active=True)
        messages.success(request, 'Done')
        return redirect('switch_session')
    context = {'session':get_session}
    return render(request, 'configuration/switch_session.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def switch_semester(request):
    get_semester = Semester.objects.all()
    if request.method == 'POST':
        semester = request.POST.get('semester')
        Semester.objects.filter(status=True).update(status=False)
        Semester.objects.filter(semester=semester).update(status=True)
        messages.success(request, 'Done')
        return redirect('switch_semester')
    context = {'semester':get_semester}
    return render(request, 'configuration/switch_semester.html',context)