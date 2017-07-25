from django.test import TestCase
from deltago.models import Commodity, Cart

from deltago.views.services import cart

class CartViewTest(TestCase):
    fixtures = [
        'deltago/fixtures/commodity.json',
        'deltago/fixtures/cart.json',
    ]

    def setUp(self):
        self.cart1 = Cart.objects.get(pk=1)
        self.cart2 = Cart.objects.get(pk=2)
        self.commodity3 = Commodity.objects.get(pk=3)

    def test_create_cart(self):
        cart3 = cart.create_cart(self.commodity3, 3)
        self.assertEqual(cart3.commodity.pk, 3)
        self.assertEqual(cart3.quantity, 3)

    def test_update_cart(self):
        cart.update_cart(self.cart1, 2)
        self.assertEqual(self.cart1.quantity, 3)

    def test_add_to_cart(self):

        data = [
            (1, 1, 2),
            (3, 1, 1),
            (20, 1, None)
        ]
        for product_id, quantity, e_result in data:
            new_cart = cart.add_to_cart(product_id, quantity)
            if new_cart:
                result = new_cart.quantity
            else:
                result = None
            self.assertEqual(result, e_result)

