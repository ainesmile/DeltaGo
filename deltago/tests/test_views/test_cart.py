from django.test import TestCase
from deltago.models import Cart

from deltago.views.services import cart

class CartServicesTest(TestCase):
    fixtures = [
        'deltago/fixtures/babycare.json',
        'deltago/fixtures/babycaredetails.json',
        'deltago/fixtures/cart.json'
    ]

    def setUp(self):
        self.cart1 = Cart.objects.get(pk=1)

    def test_update(self):
        cart.update(self.cart1, 1)
        self.assertEqual(self.cart1.quantity, 2)

    def test_add_to_cart(self):
        data = [
            ("720986", 'B', 1, 1),
            ("757788", 'B', 2, 3)
        ]
        for stockcode, category, increament, expected in data:
            cart.add_to_cart(stockcode, category, increament)
            new_cart = Cart.objects.get(stockcode=stockcode)
            self.assertEqual(new_cart.quantity, expected)


