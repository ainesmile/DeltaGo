from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def verify_user(username, password):
    current_user = User.objects.get(username=username)
    print 1111, current_user.password == password
    print authenticate(username=username, password=password)
    return authenticate(username=username, password=password) or authenticate(email=username, password=password)
