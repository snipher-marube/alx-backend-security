from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django_ratelimit.decorators import ratelimit
from django.shortcuts import render
from django.http import HttpResponseForbidden

@ratelimit(key='user_or_ip', rate='5/m', method='POST', block=True)
class RateLimitedLoginView(LoginView):
    template_name = 'registration/login.html'

    @ratelimit(key='user', rate='10/m', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Example view showing how to apply different limits to different methods
@ratelimit(key='user_or_ip', rate='5/m', block=True)
def sensitive_action(request):
    return render(request, 'sensitive_action.html')



def rate_limit_exceeded(request, exception):
    return HttpResponseForbidden(
        "Too many requests. Please try again later.",
        status=429
    )