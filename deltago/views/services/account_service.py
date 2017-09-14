# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import Q
import re
from django.core.mail import send_mail
from django.template.loader import render_to_string

from deltago.views.services import token_service, mail_service

def check_user_exist(kwargs):
    try:
        user = User.objects.get(**kwargs)
        return user
    except:
        return None


def check_user(username, password):
    user_filter = User.objects.filter(Q(username=username)|Q(email=username))
    error_message = '用户名或密码不正确'
    if user_filter:
        user = user_filter[0]
        if not user.is_active:
            need_activate = True
            error_message = '账户尚未激活'
        else:
            need_activate = False
            if user.check_password(password):
                error_message = ''
    else:
        need_activate = None
        user = None
    return error_message, need_activate, user


def verify_password(password, confirm_password):
    if not password or not confirm_password:
        return '密码不正确', False
    else:
        if password != confirm_password:
            return '两次输入的密码不一致', False
        else:
            pattern = '(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{14,}'
            if not re.match(pattern, password):
                return '密码格式不符合要求', False
            else:
                return '', True

def set_register_session(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    request.session['email'] = email
    request.session['username'] = username
    return (email, username, password, confirm_password)



def register(email, username, password, confirm_password):
    success = False
    errors = {
        "to_login": False,
        "to_activate": False,
        "username": False,
        "password": False,
        "password_message": '',
    }

    user_email = check_user_exist({"email": email})
    if user_email:
        if user_email.is_active:
            errors["to_login"] = True
        else:
            errors["to_activate"] = True
        return success, errors, user_email

    user_name = check_user_exist({"username": username})
    if user_name:
        errors["username"] = True
        return success, errors, user_name

    (error_message, is_correct) = verify_password(password, confirm_password)
    if not is_correct:
        errors["password"] = True
        errors["password_message"] = error_message
        return success, errors, None

    new_user = User(
        username=username,
        email=email,
        password=password,
        is_active=False
    )
    new_user.save()
    mail_service.send_activate_email(new_user)
    success = True
    return success, errors, new_user

def activate(uidb64, token):
    user = token_service.get_user(uidb64, token)
    if user:
        user.is_active = True
        user.save()
    return user

def activate_email(user_id):
    try:
        user = User.objects.get(pk=user_id)
        mail_service.send_activate_email(user)
        return user
    except:
        return None
    

def password_reset_email(email):
    try:
        user = User.objects.get(email=email)
    except:
        return '邮箱地址不存在。', None
    mail_service.send_password_reset_email(user)
    return '', user

def password_reset_token(uidb64, token):
    user = token_service.get_user(uidb64, token)
    return user


