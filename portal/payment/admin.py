from django.contrib import admin
from .models import Payment_setup, Payment

# Register your models here.

admin.site.register(Payment_setup)
admin.site.register(Payment)