from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ip_tracking.models import RequestLog, SuspiciousIP, BlockedIP
from django.db.models import Count

SENSITIVE_PATHS = ['/admin', '/login', '/wp-admin', '/api/auth']
REQUEST_THRESHOLD = 100  # 100 requests/hour

@shared_task
def detect_suspicious_ips():
    """
    Hourly task to detect and flag suspicious IP addresses
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Detect IPs with high request volume
    high_volume_ips = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago)
        .annotate(request_count=Count('ip_address'))
        .filter(request_count__gte=REQUEST_THRESHOLD)
    )
    
    for ip in high_volume_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip['ip_address'],
            defaults={
                'reason': 'HIGH_VOLUME',
                'details': f"Made {ip['request_count']} requests in the last hour"
            }
        )
    
    # Detect IPs accessing sensitive paths
    sensitive_access = (
        RequestLog.objects
        .filter(timestamp__gte=one_hour_ago, path__in=SENSITIVE_PATHS)
        .values('ip_address', 'path')
        .distinct()
    )
    
    for access in sensitive_access:
        SuspiciousIP.objects.get_or_create(
            ip_address=access['ip_address'],
            defaults={
                'reason': 'SENSITIVE_PATHS',
                'details': f"Accessed sensitive path: {access['path']}"
            }
        )
    
    # Return count of newly flagged IPs
    return {
        'high_volume_ips': len(high_volume_ips),
        'sensitive_access': len(sensitive_access),
    }