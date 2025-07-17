# ip_tracking/middleware.py
from django.utils import timezone
from ip_tracking.models import RequestLog

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # Get the IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Create and save the log entry
        RequestLog.objects.create(
            ip_address=ip,
            path=request.path
        )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response