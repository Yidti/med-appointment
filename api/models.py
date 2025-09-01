from django.contrib.auth.models import AbstractUser
from django.db import models

class Patient(AbstractUser):
    # Django's AbstractUser already has: username, first_name, last_name, email, password, is_staff, is_active, date_joined
    # We will use email as the primary identifier, so let's make it unique and required.
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    # We want to log in with email, so we set the USERNAME_FIELD to 'email'.
    # We also need to specify that the username field is not required anymore.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Still need username for createsuperuser, can be same as email

    def __str__(self):
        return self.email


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100) # e.g., Cardiology, Neurology
    department = models.CharField(max_length=100) # e.g., Internal Medicine
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialty}"


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'date', 'start_time')

    def __str__(self):
        return f"Dr. {self.doctor.name} on {self.date} at {self.start_time}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, related_name='appointment')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.patient.email} with Dr. {self.schedule.doctor.name} on {self.schedule.date}"


