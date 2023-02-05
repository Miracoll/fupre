from django.contrib import admin
from.models import Courses, Registered, Department_setup, Donecourse

# Register your models here.

admin.site.register(Courses)
admin.site.register(Registered)
admin.site.register(Department_setup)
admin.site.register(Donecourse)