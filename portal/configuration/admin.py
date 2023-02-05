from django.contrib import admin
from .models import Faculty, Department, User, Semester, Level, Session, Grade, Role, Config, Certification

# Register your models here.

admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(User)
admin.site.register(Semester)
admin.site.register(Level)
admin.site.register(Session)
admin.site.register(Grade)
admin.site.register(Role)
admin.site.register(Config)
admin.site.register(Certification)