from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models import Q

def check_user(username, password):
    user_filter = User.objects.filter(Q(username=username)|Q(email=username))
    if user_filter:
        user = user_filter[0]
        if user.check_password(password):
            return user
    return None
