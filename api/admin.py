from django.contrib import admin
from .models import Patient, Doctor, Schedule, Appointment

# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Schedule)
admin.site.register(Appointment)