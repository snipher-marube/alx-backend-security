from django.db import models

class RequestLog(models.Model):
    ip_address = models.CharField(max_length=45)  # Enough for IPv6
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp} - {self.path}"

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