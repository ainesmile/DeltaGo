from django.test import TestCase
from django.contrib.auth.models import User
from deltago.views.services import account

class AccountViewTest(TestCase):

    fixtures = [
        'deltago/fixtures/user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.raw_password = '11111111'

    def test_check_user(self):
        data = [
            ('admin', self.raw_password, self.user),
            ('admin@example.com', self.raw_password, self.user),
            ('wrongusername', self.raw_password, None),
            ('admin', 'wrongpassword', None),
        ]
        for username, password, e_result in data:
            result = account.check_user(username, password)
            self.assertEqual(result, e_result)

