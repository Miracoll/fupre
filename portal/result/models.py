from django.db import models
from django.utils import timezone
import uuid
from student.models import Student
from courses.models import Courses
from configuration.models import Session, Semester, User, Grade

# Create your models here.

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    ca = models.IntegerField()
    exam = models.IntegerField()
    total = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=5,blank=True,null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    lecturer = models.CharField(max_length=200, blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.total = self.ca + self.exam
        if self.total >= 70 and self.total <= 100:
            self.grade = 'A'
        elif self.total >= 60 and self.total <= 69:
            self.grade = 'B'
        elif self.total >= 50 and self.total <= 59:
            self.grade = 'C'
        elif self.total >= 45 and self.total <= 49:
            self.grade = 'D'
        elif self.total >= 40 and self.total <= 44:
            self.grade = 'E'
        elif self.total >= 0 and self.total <= 39:
            self.grade = 'F'

        super(Result, self).save(*args, **kwargs)

    def __str__(self):
        return self.student.registration_num
