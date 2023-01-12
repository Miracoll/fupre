from django.db import models
from django.utils import timezone
import uuid
from configuration.models import Faculty, Department

# Create your models here.

class Student(models.Model):
    jamb_number = models.CharField(max_length=50)
    registration_num = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100)
    entry_mode = models.CharField(max_length=20)
    level = models.IntegerField(default=100)
    entry_session = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    sex = models.CharField(max_length=10)
    dob = models.DateField()
    lock = models.BooleanField(default=False)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.registration_num