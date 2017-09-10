# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models import Q
import re

from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file

from django.core.mail import send_mail

def check_user(username, password):
    user_filter = User.objects.filter(Q(username=username)|Q(email=username))
    if user_filter:
        user = user_filter[0]
        if user.check_password(password):
            return user
    return None

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


def send_email(email):
    subject = "欢迎来到 DeltaGo"
    message = '请点击以下链接地址激活您的账户 <a href="http://deltago.ainesmile.com/activate">http://deltago.ainesmile.com/activate</a>'
    from_email = 'postmaster@mail-deltago.ainesmile.com'
    recipient_list = [email, ]
    html_message = """
        <h4>欢迎您注册 DeltaGo 请激活您的账户</h4>
        <p>请点击以下链接地址激活您的账户<a href="http://deltago.ainesmile.com/activate">http://deltago.ainesmile.com/activate</a></p>
        <small>如果您并未注册，请无视。</small>
        """
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    

def register(email, username, password, confirm_password):
    (error_msgs, is_correct) = verify_password(password, confirm_password)
    if not is_correct:
        return error_msgs, None
    if User.objects.filter(email=email):
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
    send_email(email)
    return error_msgs, new_user

