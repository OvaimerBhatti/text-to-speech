from django.shortcuts import redirect, render
from .models import Register
def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        if not request.session.get('email'):
            return redirect('/login')
        response = get_response(request)
        return response

    return middleware