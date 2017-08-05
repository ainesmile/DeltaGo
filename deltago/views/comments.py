from django.shortcuts import render
from django.contrib.auth.models import User

def comments(request):
    data = {}
    return render(request, 'deltago/comments/comments.html', data)