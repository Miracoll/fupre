from django.db import models
from django.utils import timezone
import uuid
from configuration.models import Department, Semester, Session
from student.models import Student

# Create your models here.

class Courses(models.Model):
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=200)
    credit_unit = models.IntegerField()
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10)
    level = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    coodinator = models.CharField(max_length=100, blank=True, null=True)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course_title

class Registered(models.Model):
    student = models.CharField(max_length=100)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    lock = models.BooleanField(default=False)
    credit_unit = models.IntegerField()
    semester_registered = models.ForeignKey(Semester, on_delete=models.CASCADE)
    session_registered = models.ForeignKey(Session, on_delete=models.CASCADE)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.credit_unit = self.course.credit_unit
        super(Registered, self).save(*args, **kwargs)

    def __str__(self):
        return self.student

class Department_setup(models.Model):
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.CharField(max_length=5)
    level = models.CharField(max_length=20)
    max_credit_unit = models.IntegerField()
    status = models.BooleanField(default=True)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.dept.name

class Donecourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    level = models.IntegerField()
    date_started = models.DateTimeField(default=timezone.now)
    registered_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.student.registration_num