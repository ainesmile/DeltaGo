# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import password_reset
from django.contrib.auth import update_session_auth_hash

from deltago.views.services import account_service


def login_view(request):
    redirect_to = request.GET.get('next', 'index')
    error_message = ''
    need_activate = None
    user_id = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember', None)
        error_message, need_activate, user = account_service.check_user(username, password)
        if user is not None:
            user_id = user.pk
            if not error_message:
                if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 30)
                login(request, user)
                return redirect(redirect_to)
    return render(request, 'deltago/registration/login.html', {
        "error_message": error_message,
        "need_activate": need_activate,
        "user_id": user_id,
        "redirect_to": redirect_to})


def password_reset_view(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        error_message, user = account_service.password_reset_email(email)
        if not error_message:
            return render(request, 'deltago/registration/password_reset_tips.html', {
                "email": user.email,
                "user_id": user.pk})
    return render(request, 'deltago/registration/password_reset_form.html', {"error_message": error_message})


def password_reset_repeat_view(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        return render(request, 'deltago/registration/password_reset_repeat_tips.html', {"email": user.email})
    except:
        return redirect('password_reset')
    
    
def password_reset_token_view(request, uidb64, token):
    user = account_service.password_reset_token(uidb64, token)
    if user:
        error_message = ''
        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            error_message, is_verified = account_service.verify_password(new_password1, new_password2)
            if is_verified:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                return render(request, 'deltago/registration/password_reset_done.html')
                return redirect('password_reset_done')
        return render(request, 'deltago/registration/password_reset_confirm.html', {"error_message": error_message})
    else:
        return render(request, 'deltago/registration/password_reset_invalid.html')

@login_required(login_url='login')
def password_change_view(request):
    user = request.user
    error_message = ''
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        error_message, is_verified = account_service.verify_password(new_password1, new_password2)
        if is_verified:
            old_password = request.POST.get('old_password')
            if not user.check_password(old_password):
                error_message = '您输入的密码有误，请重试'
            else:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)
                return redirect('password_change_done')
    return render(request, 'deltago/registration/password_change_form.html', {"error_message": error_message})

def register(request):
    errors = {}
    user_id = None
    if request.method == 'POST':
        email, username, password, confirm_password = account_service.set_register_session(request)
        is_success, errors, new_user = account_service.register(email, username, password, confirm_password)
        
        if new_user:
            user_id = new_user.pk

        if is_success:
            return render(request, 'deltago/registration/activate_tips.html', {
                "email": email,
                "user_id": user_id})

    return render(request, 'deltago/registration/register.html', {
        'errors': errors,
        'user_id': user_id})

def activate_view(request, uidb64, token):
    activated_user = account_service.activate(uidb64, token)
    if activated_user is None:
        return render(request, 'deltago/registration/activate_invalid.html')
    else:
        login(request, activated_user)
        return render(request, 'deltago/registration/activate_done.html')

def activate_email_view(request, user_id):
    user = account_service.activate_email(user_id)
    if user is not None:
        return render(request, 'deltago/registration/activate_tips.html', {
            "email": user.email,
            'user_id': user.pk})
    else:
        return redirect('index')

def activate_email_repeat_view(request, user_id):
    user = account_service.activate_email(user_id)
    if user is not None:
        return render(request, 'deltago/registration/activate_repeat_tips.html', {
            "email": user.email})
    else:
        return redirect('index')

def activate_email_form_view(request):
    error_message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['email'] = email
        error_message, user = account_service.activate_email_form(email)
        if user is not None:
            return render(request, 'deltago/registration/activate_tips.html', {
                "email": user.email,
                'user_id': user.pk})
    return render(request, 'deltago/registration/activate_form.html', {
        "error_message": error_message
        })


def account_delete_view(request):
    user = request.user
    if user.is_anonymous:
        raise PermissionDenied
    if request.method == 'POST':
        if account_service.check_delete_available(user):
            logout(request)
            user.delete()
            return render(request, 'deltago/registration/delete_success.html')
        else:
            return render(request, 'deltago/registration/delete_tips.html')
    else:
        return render(request, 'deltago/registration/delete.html')
    






