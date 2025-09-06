from django.core.management.base import BaseCommand
from api.models import Doctor

class Command(BaseCommand):
    help = 'Cleans up test data created for E2E testing'

    def handle(self, *args, **options):
        # Clean up the test doctor
        deleted_count, _ = Doctor.objects.filter(name='E2E Test Doctor').delete()
        if deleted_count > 0:
            self.stdout.write(self.style.SUCCESS('Successfully cleaned up test doctor data.'))
        else:
            self.stdout.write(self.style.WARNING('No E2E test doctor found to clean up.'))
