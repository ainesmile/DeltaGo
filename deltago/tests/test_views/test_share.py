from django.test import TestCase
from django.contrib.auth.models import User

from deltago.models import Commodity, Cartship

from deltago.views.services import share_service

class ShareServiceTest(TestCase):
    fixtures = [
        'deltago/fixtures/user.json',
        'deltago/fixtures/commodity.json',
        'deltago/fixtures/cart.json',
        'deltago/fixtures/cartship.json',
    ]

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.commodity1 = Commodity.objects.get(pk=1)
        self.commodity7 = Commodity.objects.get(pk=7)

        self.cartship1 = Cartship.objects.get(pk=1)
        self.cartship2 = Cartship.objects.get(pk=2)

    def test_get_commodity_price(self):
        data = [
            (self.commodity1, 209),
            (self.commodity7, 599),
        ]
        for commodity, e_price in data:
            price = share_service.get_commodity_price(commodity)
            self.assertEqual(price, e_price)

    def test_get_cartship_subtotal(self):
        data = [
            (self.cartship1, 209),
            (self.cartship2, 209*2),
        ]
        for cartship, e_subtotal in data:
            subtotal = share_service.get_cartship_subtotal(cartship)
            self.assertEqual(subtotal, e_subtotal)

    def test_get_cartships_subtotal(self):
        cartships = [self.cartship1, self.cartship2]
        e_subtotal = 209 + 209*2
        subtotal = share_service.get_cartships_subtotal(cartships)
        self.assertEqual(subtotal, e_subtotal)
        
        