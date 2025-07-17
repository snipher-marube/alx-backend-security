# ip_tracking/management/commands/block_ip.py
from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Add an IP address to the blocked list'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='IP address to block')
        parser.add_argument(
            '--remove',
            action='store_true',
            help='Remove IP from blocked list instead of adding'
        )

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        remove = options['remove']

        if remove:
            try:
                blocked_ip = BlockedIP.objects.get(ip_address=ip_address)
                blocked_ip.delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully unblocked IP: {ip_address}'))
            except BlockedIP.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'IP {ip_address} was not blocked'))
        else:
            _, created = BlockedIP.objects.get_or_create(ip_address=ip_address)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_address}'))
            else:
                self.stdout.write(self.style.WARNING(f'IP {ip_address} was already blocked'))