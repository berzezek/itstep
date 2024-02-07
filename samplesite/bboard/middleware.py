from .models import Bb

def simple_middleware(next):
    def core_middleware(request):
        response = next(request)
        print(request.readlines())
        return response
    return core_middleware

from django.contrib.auth.models import User

def all_users(request):
    return {'all_users': User.objects.all()}
