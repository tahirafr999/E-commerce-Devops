from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create admin user if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(
                self.style.SUCCESS('Successfully created admin user: admin/admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists')
            )