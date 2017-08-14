# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import password_reset
from django.contrib.auth import update_session_auth_hash

from deltago.views.services import account

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember', None)
        user = account.check_user(username, password)
        if user is not None:
            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30)
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'deltago/registration/login.html', {"wrong": True})
    else:
        return render(request, 'deltago/registration/login.html')

def password_reset_view(request):
    if request.method == 'POST':
        request.session['password_reset_email'] = request.POST.get('email')
    template_name = 'deltago/registration/password_reset_form.html',
    return password_reset(request, template_name=template_name)

def password_reset_done_view(request):
    email = request.session['password_reset_email']
    return render(request, 'deltago/registration/password_reset_done.html', {'email': email})

def password_change_view(request):
    user = request.user
    error_messages = {}
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        if not user.check_password(old_password):
            error_messages['password_incorrect'] = '您输入的密码有误，请重试'
        else:
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 and new_password2:
                if new_password1 != new_password2:
                    error_messages['password_mismatch'] = '两次输入的密码不一致'
                else:
                    user.set_password(new_password1)
                    user.save()
                    update_session_auth_hash(request, user)
                    return redirect('password_change_done')
    return render(request, 'deltago/registration/password_change_form.html', {"error_messages": error_messages})

def register(request):
    error_messages = ''
    if request.method == 'POST':
        (email, username, password, confirm_password) = account.set_register_session(request)
        error_messages, new_user = account.register_service(email, username, password, confirm_password)
        if new_user is not None:
            login(request, new_user)
            return redirect('index')
    return render(request, 'deltago/registration/register.html', {'error_messages': error_messages})

