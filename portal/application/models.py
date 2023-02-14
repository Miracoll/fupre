from email.policy import default
from django.db import models
from django.utils import timezone
from payment.models import Payment_setup
from configuration.models import Session,Department
import uuid

# Create your models here.

class Applicant(models.Model):
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    other_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    jamb = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    session = models.CharField(max_length=20)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.jamb

class Payment(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    rrr = models.CharField(max_length=20)
    payment = models.ForeignKey(Payment_setup, on_delete=models.CASCADE, related_name='applicant_payment')
    category = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    order_id = models.CharField(max_length=1000)
    amount = models.IntegerField()
    session = models.CharField(max_length=20)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    generated_on = models.DateTimeField(default=timezone.now)
    paid_on = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.rrr

class Personal(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    other_name = models.CharField(max_length=20,blank=True,null=True)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    jamb = models.CharField(max_length=20)
    address = models.TextField(max_length=200,blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=10,blank=True,null=True)
    photo = models.ImageField(default='passport.jpg', upload_to='Application')
    session = models.CharField(max_length=20)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.applicant.jamb

class Course(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    dept1 = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='applicat_first_choice')
    dept2 = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='applicat_second_choice')
    session = models.CharField(max_length=20)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.applicant.jamb

class NOK(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=100,blank=True, null=True)
    mobile = models.CharField(max_length=20,blank=True,null=True)
    relationship = models.CharField(max_length=20,blank=True,null=True)
    address = models.TextField(max_length=200,blank=True,null=True)
    session = models.CharField(max_length=20,blank=True,null=True)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.applicant.jamb

class Olevel(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=100)
    exam_number = models.CharField(max_length=100,blank=True, null=True)
    exam_year = models.CharField(max_length=20)
    exam_center = models.CharField(max_length=20)
    sub1 = models.CharField(max_length=50)
    grade1 = models.CharField(max_length=5)
    sub2 = models.CharField(max_length=50)
    grade2 = models.CharField(max_length=5)
    sub3 = models.CharField(max_length=50)
    grade3 = models.CharField(max_length=5)
    sub4 = models.CharField(max_length=50)
    grade4 = models.CharField(max_length=5)
    sub5 = models.CharField(max_length=50)
    grade5 = models.CharField(max_length=5)
    sub6 = models.CharField(max_length=50)
    grade6 = models.CharField(max_length=5)
    sub7 = models.CharField(max_length=50)
    grade7 = models.CharField(max_length=5)
    sub8 = models.CharField(max_length=50)
    grade8 = models.CharField(max_length=5)
    sub9 = models.CharField(max_length=50)
    grade9 = models.CharField(max_length=5)
    session = models.CharField(max_length=20)

    exam_type2 = models.CharField(max_length=100,blank=True, null=True)
    exam_number2 = models.CharField(max_length=100,blank=True, null=True)
    exam_year2 = models.CharField(max_length=20,blank=True, null=True)
    exam_center2 = models.CharField(max_length=20,blank=True, null=True)
    sub12 = models.CharField(max_length=50,blank=True, null=True)
    grade12 = models.CharField(max_length=5,blank=True, null=True)
    sub22 = models.CharField(max_length=50,blank=True, null=True)
    grade22 = models.CharField(max_length=5,blank=True, null=True)
    sub32 = models.CharField(max_length=50,blank=True, null=True)
    grade32 = models.CharField(max_length=5,blank=True, null=True)
    sub42 = models.CharField(max_length=50,blank=True, null=True)
    grade42 = models.CharField(max_length=5,blank=True, null=True)
    sub52 = models.CharField(max_length=50,blank=True, null=True)
    grade52 = models.CharField(max_length=5,blank=True, null=True)
    sub62 = models.CharField(max_length=50,blank=True, null=True)
    grade62 = models.CharField(max_length=5,blank=True, null=True)
    sub72 = models.CharField(max_length=50,blank=True, null=True)
    grade72 = models.CharField(max_length=5,blank=True, null=True)
    sub82 = models.CharField(max_length=50,blank=True, null=True)
    grade82 = models.CharField(max_length=5,blank=True, null=True)
    sub92 = models.CharField(max_length=50,blank=True, null=True)
    grade92 = models.CharField(max_length=5,blank=True, null=True)
    session = models.CharField(max_length=20)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.applicant.jamb

class Admitted(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    session = models.CharField(max_length=20)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.applicant.jamb

class Acceptance(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    rrr = models.CharField(max_length=20)
    payment = models.ForeignKey(Payment_setup, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    amount = models.IntegerField()
    order_id = models.CharField(max_length=1000)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    session = models.CharField(max_length=20)
    generated_on = models.DateTimeField(default=timezone.now)
    paid_on = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.applicant.jamb

class Document(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    olevel1 = models.ImageField(upload_to='Document')
    olevel2 = models.ImageField(upload_to='Document',blank=True,null=True)
    birth = models.ImageField(upload_to='Document')
    lga = models.ImageField(upload_to='Document')
    jamb_result = models.ImageField(upload_to='Document')

    def __str__(self) -> str:
        return self.applicant.jamb

class Student(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE,blank=True,null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,blank=True,null=True)
    olevel = models.ForeignKey(Olevel, on_delete=models.CASCADE,blank=True,null=True)
    nok = models.ForeignKey(NOK, on_delete=models.CASCADE,blank=True,null=True)
    registration_num = models.CharField(max_length=100,blank=True,null=True)
    cleared = models.BooleanField(default=False)
    admitted = models.BooleanField(default=False)
    level = models.IntegerField(default=0)
    session = models.CharField(max_length=20)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.applicant.jamb