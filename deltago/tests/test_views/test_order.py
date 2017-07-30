from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from deltago.exceptions import errors
from deltago.models import Cartship, Cart, Commodity, Order

from deltago.views.services import order


class OrderViewTest(TestCase):
    fixtures = [
        'deltago/fixtures/user.json',
        'deltago/fixtures/commodity.json',
        'deltago/fixtures/cart.json',
        'deltago/fixtures/cartship.json',
    ]

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.cart = Cart.objects.get(pk=1)
        self.all_cartshipes = Cartship.objects.all()
        self.cartship1 = Cartship.objects.get(pk=1)
        self.cartship2 = Cartship.objects.get(pk=2)
        self.commodity = Commodity.objects.get(pk=1)
        self.price = 209

        self.checkboxes = [1]
        self.quantities = [5, 10]


    def test_undelete_cartship(self):
        cartshipes = [self.cartship1, self.cartship2]
        for cartship in cartshipes:
            order.undelete_cartship(cartship)
            self.assertFalse(cartship.is_deleted)

    def test_choose_cartship(self):
        order.choose_cartship(self.cartship1)
        self.assertTrue(self.cartship1.is_chosen)

    def test_get_chosen_cartshipes(self):
        chosens = order.get_chosen_cartshipes(self.checkboxes)
        self.assertEqual(chosens, [self.cartship1])

    def test_get_unchosen_cartshipes(self):
        chosens = [self.cartship1]
        unchosen = order.get_unchosen_cartshipes(self.all_cartshipes, chosens)
        self.assertEqual(unchosen, [self.cartship2])

    def test_update_quantities(self):
        quantities = self.quantities
        order.update_quantities(self.all_cartshipes, quantities)
        for index, cartship in enumerate(self.all_cartshipes):
            quantity = quantities[index]
            self.assertEqual(cartship.quantity, quantity)

    # def test_archive_cart(self):
    #     order.archive_cart(self.cart)
    #     self.assertTrue(self.cart.is_archived)

    def test_new_cart_with_unchosens(self):
        unchosens = [self.cartship2]
        order.new_cart_with_unchosens(self.admin, unchosens)

    def test_get_price(self):
        price = order.get_price(self.commodity)
        self.assertEqual(price, self.price)

    def test_get_commodity_total(self):
        commodity_total = order.get_commodity_total(self.cartship1)
        self.assertEqual(commodity_total, self.price)

    def test_get_subtotal(self):
        subtotal = order.get_subtotal(self.all_cartshipes)
        self.assertEqual(subtotal, 209*3)

    def test_init_order(self):
        subtotal = 209*3
        total = 209*3+500
        order.init_order(self.cart, subtotal, total)
        new_order = Order.objects.get(cart=self.cart)
        self.assertEqual(new_order.user, self.admin)
        self.assertEqual(new_order.subtotal, subtotal)
        self.assertEqual(new_order.total, total)

    def test_create_order_by_chosen(self):
        chosens = [self.cartship1]
        subtotal = 209
        total = 209 + 500
        order.create_order_by_chosen(self.cart, chosens)
        new_order = Order.objects.get(cart=self.cart)
        self.assertEqual(new_order.user, self.cart.user)
        self.assertEqual(new_order.cart, self.cart)
        self.assertEqual(new_order.subtotal, subtotal)
        self.assertEqual(new_order.total, total)

    def test_generate_order(self):
        user = self.admin
        quantities = self.quantities
        checkboxes_data = [self.checkboxes, []]
        for checkboxes in checkboxes_data:
            try:
                order.generate_order(user, checkboxes, quantities)
                updated_cart = Cart.objects.get(pk=1)
                self.assertTrue(updated_cart.is_archived)
                new_order = Order.objects.last()
                self.assertEqual(new_order.user, user)
                self.assertEqual(new_order.cart, updated_cart)
            except errors.EmptyCartError as e:
                self.assertTrue(isinstance(e, errors.EmptyCartError))



        

