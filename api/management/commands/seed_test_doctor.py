from django.core.management.base import BaseCommand
from api.models import Doctor, Schedule
from datetime import date, timedelta, time

class Command(BaseCommand):
    help = 'Seeds the database with a specific doctor for E2E testing'

    def handle(self, *args, **options):
        # Clean up any previous test doctor
        Doctor.objects.filter(name='E2E Test Doctor').delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleaned up old test doctors.'))

        # Create the test doctor
        test_doctor = Doctor.objects.create(
            name='E2E Test Doctor',
            specialty='E2E Testing',
            department='QA'
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully created doctor: {test_doctor.name}'))

        # Create a schedule for tomorrow
        tomorrow = date.today() + timedelta(days=1)
        Schedule.objects.create(
            doctor=test_doctor,
            date=tomorrow,
            start_time=time(10, 0),
            end_time=time(10, 30),
            is_available=True
        )
        Schedule.objects.create(
            doctor=test_doctor,
            date=tomorrow,
            start_time=time(11, 0),
            end_time=time(11, 30),
            is_available=True
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created schedule for {test_doctor.name} on {tomorrow}'))
