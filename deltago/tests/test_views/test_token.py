from django.test import TestCase
from django.contrib.auth.models import User

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from deltago.views.services import token_service

class TokenTest(TestCase):
    fixtures = [
        'deltago/fixtures/user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)

    def test_uid_generate_and_decode(self):
        uidb64 = token_service.uid_generate(self.user)
        username = token_service.uid_decode(uidb64)
        self.assertEqual(username, self.user.username)

    def test_token_generate_and_check(self):
        token = token_service.token_generate(self.user)
        self.assertTrue(token_service.token_check(self.user, token))

    def test_get_user(self):
        uidb64 = token_service.uid_generate(self.user)
        token = token_service.token_generate(self.user)
        data = [
            (uidb64, token, self.user),
            ('uidb64', 'token', None)
        ]
        for uidb64, token, e_user in data:
            user = token_service.get_user(uidb64, token)
            self.assertEqual(user, e_user)

