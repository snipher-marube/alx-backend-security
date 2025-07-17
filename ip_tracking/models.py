from django.db import models

class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        location = f"{self.city}, {self.country}" if self.city and self.country else "Unknown location"
        return f"{self.ip_address} ({location}) - {self.timestamp} - {self.path}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Request Log'
        verbose_name_plural = 'Request Logs'

class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = 'Blocked IP'
        verbose_name_plural = 'Blocked IPs'

class SuspiciousIP(models.Model):
    REASON_CHOICES = [
        ('HIGH_VOLUME', 'High request volume'),
        ('SENSITIVE_PATHS', 'Accessed sensitive paths'),
        ('MULTIPLE_REASONS', 'Multiple suspicious activities'),
    ]
    
    ip_address = models.CharField(max_length=45)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.ip_address} - {self.get_reason_display()}"

    class Meta:
        verbose_name = 'Suspicious IP'
        verbose_name_plural = 'Suspicious IPs'
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['timestamp']),
        ]