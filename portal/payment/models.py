from django.db import models
from django.utils import timezone
import uuid
from configuration.models import Semester, Session
from student.models import Student

# Create your models here.

class Payment_setup(models.Model):
    payment_type = models.CharField(max_length=150)
    amount = models.IntegerField()
    category = models.CharField(max_length=100)
    level = models.CharField(max_length=20, default='all')
    ref = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.payment_type

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rrr = models.CharField(max_length=20)
    payment = models.ForeignKey(Payment_setup, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    order_id = models.CharField(max_length=1000)
    level = models.IntegerField(default=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    generated_on = models.DateTimeField(default=timezone.now)
    paid_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.rrr