from django.test import TestCase
from django.contrib.auth.models import User

from deltago.models import Commodity, Cartship

from deltago.views.services import share_service

class ShareServiceTest(TestCase):
    fixtures = [
        'deltago/fixtures/user.json',
        'deltago/fixtures/products.json',
        'deltago/fixtures/details.json',
        'deltago/fixtures/cart.json',
        'deltago/fixtures/cartship.json',
    ]

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.commodity1 = Commodity.objects.get(pk=1)

        self.cartship1 = Cartship.objects.get(pk=1)
        self.cartship2 = Cartship.objects.get(pk=2)

    def test_cal_ship_fee(self):
        cartships = [self.cartship1, self.cartship2]
        result = share_service.cal_ship_fee(cartships)
        e_result = round(500 * (float(603*1 + 1144*2 + 200)/1000), 2)
        self.assertEqual(result, e_result)

    def test_get_cartship_subtotal(self):
        data = [
            (self.cartship1, 650),
            (self.cartship2, 1849*2),
        ]
        for cartship, e_subtotal in data:
            subtotal = share_service.get_cartship_subtotal(cartship)
            self.assertEqual(subtotal, e_subtotal)

    def test_get_cartships_subtotal(self):
        cartships = [self.cartship1, self.cartship2]
        e_subtotal = 650 + 1849*2
        subtotal = share_service.get_cartships_subtotal(cartships)

        self.assertEqual(subtotal, e_subtotal)
        
        