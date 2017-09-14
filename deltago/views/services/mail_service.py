# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.template.loader import render_to_string

from deltago.views.services import token_service

def mail_url(base, user):
    uidb64 = token_service.uid_generate(user)
    token = token_service.token_generate(user)
    url = base + uidb64 + "/" + token
    return url

def send_email(content, user):
    (subject, message, html_message) = content
    from_email = 'postmaster@mail-deltago.ainesmile.com'
    recipient_list = [user.email, ]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

def generate_activate_email_content(user):
    base_url = 'http://deltago.ainesmile.com/activate/'
    url = mail_url(base_url, user)
    subject = "欢迎来到 DeltaGo"
    message = '<a href="%s">%s</a>' % (url, url)
    html_message = render_to_string('deltago/registration/activate_email.html', {
        "user": user,
        "activate_url": url
        })
    return (subject, message, html_message)

def geterate_password_reset_email_content(user):
    base_url = 'http://deltago.ainesmile.com/password/reset/'
    url = mail_url(base_url, user)
    subject = "请重置您的密码"
    message = '<a href="%s">%s</a>' % (url, url)
    html_message = render_to_string('deltago/registration/password_reset_email.html', {
        "password_reset_email_url": url})
    return (subject, message, html_message)


def send_activate_email(user):
    content = generate_activate_email_content(user)
    send_email(content, user)

def send_password_reset_email(user):
    content = geterate_password_reset_email_content(user)
    send_email(content, user)


