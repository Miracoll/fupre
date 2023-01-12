from django.db import models
from django.utils import timezone
import uuid
from configuration.models import Department, Semester, Level, Session

# Create your models here.

class Courses(models.Model):
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=200)
    credit_unit = models.IntegerField()
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
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
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    level = models.CharField(max_length=20)
    max_credit_unit = models.IntegerField()
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.dept.name