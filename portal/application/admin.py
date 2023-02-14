from django.contrib import admin
from .models import Applicant,Payment,Personal,Course,NOK,Olevel,Admitted,Acceptance,Student,Document

# Register your models here.

admin.site.register(Applicant)
admin.site.register(Payment)
admin.site.register(Personal)
admin.site.register(Course)
admin.site.register(NOK)
admin.site.register(Olevel)
admin.site.register(Admitted)
admin.site.register(Acceptance)
admin.site.register(Student)
admin.site.register(Document)