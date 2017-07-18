from django.test import TestCase, Client
from django.core.paginator import Page
from deltago.models import Cart

from deltago.views.services import cart

class CartServicesTest(TestCase):
    fixtures = [
        'deltago/fixtures/babycare.json',
        'deltago/fixtures/babycaredetails.json',
        'deltago/fixtures/cart.json'
    ]

    def setUp(self):
        client = Client()
        self.request = client.get('cart').wsgi_request
        self.page = 1
        self.cart1 = Cart.objects.get(pk=1)

    def test_update(self):
        cart.update(self.cart1, 1)
        self.assertEqual(self.cart1.quantity, 2)

    def test_add_to_cart(self):
        data = [
            (1, 'B', 1, 2),
            (3, 'B', 2, 2)
        ]
        for commodity_id, category, increament, expected in data:
            cart.add_to_cart(commodity_id, category, increament)
            updated_cart = Cart.objects.get(pk=commodity_id)
            self.assertEqual(updated_cart.quantity, expected)

    def test_get_product(self):
        product = cart.get_product(self.cart1)
        self.assertEqual(product.pk, 1)

    def test_get_cart_item(self):
        item = cart.get_cart_item(self.cart1)
        self.assertEqual(item.quantity, 1)

    def test_cart_list(self):
        data = cart.cart_list(self.page, 20)
        self.assertTrue(isinstance(data["paginations"], Page))
        self.assertTrue(isinstance(data["products"], Page))
