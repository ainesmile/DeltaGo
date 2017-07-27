from django.test import TestCase, Client
from django.core.paginator import Page
from django.contrib.auth.models import User
from deltago.models import Commodity, Cart, Cartship

from deltago.views.services import cart

class CartViewTest(TestCase):
    fixtures = [
        'deltago/fixtures/commodity.json',
        'deltago/fixtures/cart.json',
        'deltago/fixtures/user.json',
        'deltago/fixtures/cartship.json'
    ]

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.user1 = User.objects.get(pk=2)
        self.cartship = Cartship.objects.get(pk=1)
        self.cart = Cart.objects.get(pk=1)
        self.commodity =  Commodity.objects.get(pk=1)
        self.commodity3 = Commodity.objects.get(pk=3)


        client = Client()
        response = client.get('cart')
        request = response.wsgi_request
        self.page = request.GET.get('page', 1)
        

    def test_get_user_cart(self):
        user_cart = cart.get_user_cart(self.admin)
        self.assertEqual(user_cart.user, self.admin)

    def test_get_commodity(self):
        data = [
            (1, self.commodity),
            (11, None)
        ]
        for product_id, e_commodity in data:
            commodity = cart.get_commodity(product_id)
            self.assertEqual(commodity, e_commodity)

    def test_update_cartship_quantity(self):
        cart.update_cartship_quantity(self.cartship, 2)
        self.assertEqual(self.cartship.quantity, 3)

    def test_update_or_create_cartship(self):
        data = [
            (self.commodity, 2, 3),
            (self.commodity3, 1, 1),
        ]
        for commodity, quantity, e_quantity in data:
            cartship = cart.update_or_create_cartship(self.cart, commodity, quantity)
            self.assertEqual(cartship.quantity, e_quantity)

    def test_add_to_cart(self):
        data = [
            (1, 1, self.cartship),
            (13, 1, None)
        ]
        for product_id, quantity, e_result in data:
            result = cart.add_to_cart(self.admin, product_id, quantity)
            self.assertEqual(result, e_result)

    def test_cart_list(self):
        result = cart.cartship_list(self.admin, self.page, 20)
        self.assertTrue(isinstance(result["cartshipes"], Page))
