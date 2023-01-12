from django.contrib import admin
from .models import Faculty, Department, User, Semester, Level, Session

# Register your models here.

admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(User)
admin.site.register(Semester)
admin.site.register(Level)
admin.site.register(Session)