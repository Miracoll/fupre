from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Bedspace, Floor, Hostel, Occupant, Room
from payment.models import Payment
from student.models import Student
from configuration.models import Semester,Session

# Create your views here.

def viewhostel(request):
    student = Student.objects.get(registration_num=request.user.username)
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    if not Payment.objects.filter(student=student,category='hostel',semester=semester,session=session,status=True).exists():
        messages.error(request, 'No hostel payment found')
        return redirect('payment')
    if Occupant.objects.filter(student=student.registration_num,session=session.session,semester=semester.semester).exists():
        ref = Occupant.objects.get(student=student.registration_num,session=session.session,semester=semester.semester).ref
        return redirect('hostelprintout',ref)
    get_payment_type = Payment.objects.get(student=student,category='hostel',semester=semester,session=session).payment.payment_type
    hostel = Hostel.objects.get(hostel_name=get_payment_type)
    bedspace = Bedspace.objects.filter(hostel=hostel, lock=0, active = 1)
    context = {'bedspace':bedspace,'hostel':hostel}
    return render(request, 'hostel/viewhostel.html', context)

def assign2occupant(request, pk):
    student = Student.objects.get(registration_num=request.user.username)
    semester = Semester.objects.get(status=True)
    session = Session.objects.get(active=True)
    occupant = Payment.objects.get(student=student,semester=semester,session=session,category='hostel').student.registration_num
    bedspace = Bedspace.objects.filter(ref=pk)
    getbedspace = Bedspace.objects.get(ref=pk)
    floor = Bedspace.objects.get(ref=pk).floor
    if request.method == 'POST':
        # Arithemetic
        room = getbedspace.room
        get_occupied1 = int(room.occupied)
        Room.objects.filter(id=room.id,active=1,lock=0).update(occupied=get_occupied1+1)
        get_occupied2 = int(room.occupied)
        get_space = room.occupant_per_room - get_occupied2
        Room.objects.filter(id=room.id,active=1,lock=0).update(
            space_available = get_space-1
        )

        # Lock room if filled up
        if room.space_available == 0 and room.occupied == room.occupant_per_room:
            Room.objects.filter(floor=floor,active=1,lock=0).update(lock=True,available=False)

        # Lock bedspace if taken
        bedspace.update(lock=1,occupied=1)

        # Lock floor if filled up
        if not Room.objects.filter(floor_id=floor.id,lock=0).exists():
            Floor.objects.filter(id=floor.id).update(lock=1)

        # Lock hostel if filled up
        if not Floor.objects.filter(hostel_id=floor.id,lock=0).exists():
            Floor.objects.filter(id=floor.id).update(lock=1)
        
        # Add to occupant table
        amount = Payment.objects.get(student=student,semester=semester,session=session,category='hostel').payment.amount
        Occupant.objects.create(
            student=occupant,amount_paid=amount,bedspace=getbedspace,semester=semester.semester,session=session.session,
            created_by=request.user
        )
        getprint = Occupant.objects.get(session=session.session,semester=semester.semester,student=occupant).ref
        messages.success(request, 'Allocation successful')
        return redirect('hostelprintout',getprint)
    context = {'bedspace':bedspace}
    return render(request, 'hostel/assignoccupant.html', context)

def hostelprintout(request,pk):
    get_student = Occupant.objects.get(ref=pk).student
    student = Student.objects.filter(registration_num=get_student)
    hostel = Occupant.objects.filter(ref=pk)
    context = {'hostel':hostel,'student':student}
    return render(request, 'hostel/printout.html',context)