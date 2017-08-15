# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
import re
from deltago.views.services import account_service

class AccountViewTest(TestCase):

    fixtures = [
        'deltago/fixtures/user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.raw_password = '11111111'
        self.register_password = '11111aaaaaAAAAA'
        self.error_msgs_email = '该邮箱已经被注册'
        self.error_msgs_username = '用户名已存在'
        self.error_msgs_password = '密码格式不符合要求'

    def test_check_user(self):
        data = [
            ('admin', self.raw_password, self.user),
            ('admin@example.com', self.raw_password, self.user),
            ('wrongusername', self.raw_password, None),
            ('admin', 'wrongpassword', None),
        ]
        for username, password, e_result in data:
            result = account_service.check_user(username, password)
            self.assertEqual(result, e_result)

    def test_verify_password(self):
        data = [
            ('', '1', '密码不正确', False),
            ('1', '2', '两次输入的密码不一致', False),
            ('0123456789', '0123456789', '密码格式不符合要求', False),
            ('01234567891234', '01234567891234', '密码格式不符合要求', False),
            ('0123456789abcd', '0123456789abcd', '密码格式不符合要求', False),
            (self.register_password, self.register_password, '', True)
        ]
        for password, confirm_password, e_msg, e_result in data:
            (msg, result) = account_service.verify_password(password, confirm_password)
            self.assertEqual(msg, e_msg)
            self.assertEqual(result, e_result)

    def test_register(self):
        data = [
            ('admin@example.com', 'admin', 'password', 'password', self.error_msgs_password, None),
            ('admin@example.com', 'admin', self.register_password, self.register_password, self.error_msgs_email, None),
            ('1@1.com', 'admin', self.register_password, self.register_password, self.error_msgs_username, None),
            ('1@1.com', '1', self.register_password, self.register_password, '', True)
        ]
        for email, username, password, confirm_password, e_msg, e_user in data:
            (msg, user) = account_service.register(email, username, password, confirm_password)
            self.assertEqual(msg, e_msg)
            self.assertEqual(bool(user), bool(e_user))
