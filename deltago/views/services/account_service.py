# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import Q
import re
from django.core.mail import send_mail
from django.template.loader import render_to_string

from deltago.views.services import token_service, mail_service


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


def set_register_session(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    request.session['email'] = email
    request.session['username'] = username
    return (email, username, password, confirm_password)

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

def register(email, username, password, confirm_password):
    (error_msgs, is_correct) = verify_password(password, confirm_password)
    if not is_correct:
        return error_msgs, None
    if User.objects.filter(email=email, is_active=True):
        return '该邮箱已经被注册', None
    if User.objects.filter(username=username):
        return '用户名已存在', None
    new_user = User(
        username=username,
        email=email,
        password=password,
        is_active=False
    )
    new_user.save()
    mail_service.send_activate_email(new_user)
    return error_msgs, new_user


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


