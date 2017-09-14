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
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.raw_password = '11111111'
        self.error_msg_activate = '账户尚未激活'
        self.error_msg_username = '用户名或密码不正确'

        self.register_password = '11111aaaaaAAAAA'

    def test_check_user(self):
        data = [
            (self.user1.username, self.raw_password, '', False, self.user1),
            (self.user2.username, self.raw_password, self.error_msg_activate, True, self.user2),
            (self.user1.email, 'wrongpassword', self.error_msg_username, False, self.user1),
            ('wrongusername', 'wrongpassword', self.error_msg_username, None, None),
        ]
        for username, password, e_msg, e_need, e_user in data:
            msg, need, user = account_service.check_user(username, password)
            self.assertEqual(msg, e_msg)
            self.assertEqual(need, e_need)
            self.assertEqual(user, e_user)

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

