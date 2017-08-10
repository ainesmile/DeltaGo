from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import password_reset

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'deltago/account/login.html', {"wrong": True}) 
    else:
        return render(request, 'deltago/account/login.html')

def password_reset_view(request):
    if request.method == 'POST':
        request.session['password_reset_email'] = request.POST.get('email')
    template_name = 'deltago/registration/password_reset_form.html',
    return password_reset(request, template_name=template_name)

def password_reset_done_view(request):
    email = request.session['password_reset_email']
    return render(request, 'deltago/registration/password_reset_done.html', {'email': email})

