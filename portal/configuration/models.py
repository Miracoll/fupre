from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.template.defaultfilters import slugify
import uuid

# Create your models here.

class Config(models.Model):
    school_name = models.CharField(max_length=100, blank=True, null=True)
    school_initial = models.CharField(max_length=5, blank=True, null=True)
    school_domain_name = models.CharField(max_length=255, blank=True, null=True)
    school_logo = models.ImageField(blank=True, null=True, upload_to='configuration')
    course_reg_status = models.BooleanField(default=False)
    course_start_date = models.DateField(blank=True, null=True)
    course_end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.school_name

class Role(models.Model):
    role = models.CharField(max_length=30)
    keyword = models.SlugField()
    active = models.IntegerField(default=1)
    created_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.keyword = slugify(self.role)
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return self.role

class User(AbstractUser):
    image = models.ImageField(upload_to='passport', default='passport.jpg', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    lock_reason = models.TextField(max_length=2000, blank=True, null=True)
    defer = models.BooleanField(default=False)
    password_reset = models.BooleanField(default=False)

class Faculty(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    dean = models.CharField(max_length=255)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    dept_abbr = models.CharField(max_length=5)
    code = models.CharField(max_length=50)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    hod = models.CharField(max_length=255)
    max_level = models.IntegerField(default=400)
    number_of_years = models.IntegerField(default=4)
    cert = models.CharField(max_length=10)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.number_of_years = int(int(self.max_level)/100)
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Semester(models.Model):
    semester = models.IntegerField(default=1)
    status = models.BooleanField(default=False)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.semester)

    class Meta:
        ordering = ['semester']

class Session(models.Model):
    session = models.CharField(max_length=20)
    year = models.CharField(max_length=4)
    active = models.BooleanField(default=True)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.session)

    class Meta:
        ordering = ['year']

class Level(models.Model):
    level = models.IntegerField(default=100)
    active = models.BooleanField(default=True)
    ref = models.UUIDField(default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.level)

    class Meta:
        ordering = ['level']

class Grade(models.Model):
    grade = models.CharField(max_length=5)
    description = models.CharField(max_length=20)
    max_score = models.IntegerField()
    min_score = models.IntegerField()
    point = models.IntegerField()
    ref = models.UUIDField(default=uuid.uuid4, editable=False)

class Certification(models.Model):
    name = models.CharField(max_length=200)
    abb = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name