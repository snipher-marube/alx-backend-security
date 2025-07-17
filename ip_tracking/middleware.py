# ip_tracking/middleware.py
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.utils import timezone
from ip_tracking.models import RequestLog, BlockedIP
from ipgeolocation import IpGeolocationAPI

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Initialize with your API key (you should add this to settings.py)
        self.geolocation_api = IpGeolocationAPI()

    def __call__(self, request):
        # Get the IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Check if IP is blocked
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP address has been blocked.")

        # Get geolocation data (with caching)
        cache_key = f'ip_geo_{ip}'
        geo_data = cache.get(cache_key)
        
        if not geo_data:
            try:
                geo_data = self.geolocation_api.get_geolocation(ip_address=ip)
                if geo_data.get('status') == 'success':
                    # Cache for 24 hours (86400 seconds)
                    cache.set(cache_key, geo_data, 86400)
                else:
                    geo_data = None
            except Exception as e:
                # Log error but don't break the request
                print(f"Geolocation API error: {e}")
                geo_data = None

        # Create log entry
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path,
            country=geo_data.get('country_name') if geo_data else None,
            city=geo_data.get('city') if geo_data else None
        )

        response = self.get_response(request)
        return response