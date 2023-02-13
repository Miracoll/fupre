from django.shortcuts import redirect, render
from result.models import Result
from student.models import Student
from configuration.models import Session, Semester

# Create your views here.

def get_result(request):
    all_session = Session.objects.all()
    if request.method == 'POST':
        session = request.POST.get('session')
        semester = request.POST.get('semester')
        get_session = Session.objects.get(session=session).ref
        get_semester = Semester.objects.get(semester=semester).ref
        return redirect('result', get_session, get_semester)
    context = {'session':all_session}
    return render(request, 'result/get_student.html',context)

def result(request, isession, isemester):
    student = Student.objects.get(registration_num=request.user.username)
    semester = Semester.objects.get(ref=isemester)
    session = Session.objects.get(ref=isession)
    result = Result.objects.filter(student=student,session=session,semester=semester)
    context = {'result':result, 'student':student, 'semester':semester, 'session':session }
    return render(request, 'result/result.html',context)