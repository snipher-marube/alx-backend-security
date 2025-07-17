from django.urls import path
from ip_tracking.views import RateLimitedLoginView

urlpatterns = [
    
    path('accounts/login/', RateLimitedLoginView.as_view(), name='login'),
    
]