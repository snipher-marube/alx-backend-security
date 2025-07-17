from django.core.management.base import BaseCommand
from ip_tracking.tasks import detect_suspicious_ips

class Command(BaseCommand):
    help = 'Manually run suspicious IP detection'

    def handle(self, *args, **options):
        result = detect_suspicious_ips.delay()
        self.stdout.write(self.style.SUCCESS(f'Scheduled suspicious IP detection: {result.id}'))