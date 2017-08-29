# -*- coding: utf-8 -*-
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from deltago.exceptions import errors
from deltago.models import Cartship, Cart, Commodity, Order

from deltago.views.services import order_service


class OrderViewTest(TestCase):
    fixtures = [
        'deltago/fixtures/user.json',
        'deltago/fixtures/products.json',
        'deltago/fixtures/details.json',
        'deltago/fixtures/cart.json',
        'deltago/fixtures/cartship.json',
        'deltago/fixtures/order.json',
    ]


    def setUp(self):

        self.admin = User.objects.get(pk=1)
        self.cart = Cart.objects.get(pk=1)
        self.all_cartships = Cartship.objects.all()
        self.cartship1 = Cartship.objects.get(pk=1)
        self.cartship2 = Cartship.objects.get(pk=2)
        self.commodity = Commodity.objects.get(pk=1)
        self.price = 650

        self.checkboxes = [1]
        self.quantities = [5, 10]

        self.order = Order.objects.get(pk=1)

        self.e_fee = {
            "subtotal": 836,
            "total": 1336,
            "ship_fee": 500,
            "exchange_rate": 500
        }

        self.e_commodity_info_table_item = {
            "commodity": self.commodity,
            "price": 650,
            "quantity": 1,
            "commodity_total": 650
        }


    def test_update_cartships(self):
        data = [
            ([u'1'], False),
            ([u'1'], True),
        ]
        for checkboxes, checkbox_all in data:
            updated_cartships = order_service.update_cartships(
                self.cart, checkboxes, self.quantities, checkbox_all)
            for index, updated in enumerate(updated_cartships):
                self.assertEqual(updated.quantity, self.quantities[index])
                if (updated.pk in checkboxes) or checkbox_all:
                    self.assertEqual(updated.is_deleted, False)
                    self.assertEqual(updated.is_chosen, True)

    def test_archive_cart(self):
        order_service.archive_cart(self.cart)
        self.assertTrue(self.cart.is_archived)

    def test_generate_order_serial_code(self):
        serial_code = order_service.generate_order_serial_code(self.order)
        self.assertEqual(len(serial_code), 20)

    def test_init_order(self):
        subtotal = 650*3
        total = 650*3+500
        new_order = order_service.init_order(self.cart, subtotal, total)
        self.assertEqual(new_order.user, self.admin)
        self.assertEqual(new_order.subtotal, subtotal)
        self.assertEqual(new_order.total, total)

    def test_new_order_with_chosen(self):
        chosens = [self.cartship1]
        subtotal = 650 * 1
        weight = max((float(603 * 1 + 200)/1000), 1.0)
        ship_fee = round(500 * weight, 2)
        total = subtotal + ship_fee

        new_order = order_service.new_order_with_chosen(self.cart, chosens)
        self.assertEqual(new_order.user, self.cart.user)
        self.assertEqual(new_order.cart, self.cart)
        self.assertEqual(new_order.subtotal, subtotal)
        self.assertEqual(new_order.total, total)

    def test_new_cart_with_unchosens(self):
        unchosens = [self.cartship2]
        new_cart = order_service.new_cart_with_unchosens(self.admin, unchosens)
        self.assertEqual(self.cartship2.cart, new_cart)

    def test_get_order_show_fee(self):
        fee = order_service.get_order_show_fee(self.order)
        self.assertEqual(fee, self.e_fee)

    def test_get_order_state_text(self):
        text = order_service.get_order_state_text(self.order.state)
        self.assertEqual(text, '未支付')

    def test_get_order_basic_info(self):
        order = order_service.get_order_basic_info(self.order)
        self.assertEqual(order.fee, self.e_fee)
        self.assertEqual(order.state_text, '未支付')

    def test_get_commodity_info_table_item(self):
        item = order_service.get_commodity_info_table_item(self.cartship1)
        self.assertEqual(item, self.e_commodity_info_table_item)

    def test_get_commodity_info_table(self):
        data = [
            (1, 650, 1, 650),
            (2, 1849, 2, 3698)
        ]
        table = order_service.get_commodity_info_table(self.order)
        for index, item in enumerate(table):
            data_item = data[index]
            self.assertEqual(item["commodity"].pk, data_item[0])
            self.assertEqual(item["price"], data_item[1])
            self.assertEqual(item["quantity"], data_item[2])
            self.assertEqual(item["commodity_total"], data_item[3])

    def test_generate_order(self):
        user = self.admin
        quantities = self.quantities
        data = [
            (self.checkboxes, False),
            (self.checkboxes, True),
            ([], True),
            ([], False),
        ]
        for checkboxes, checkbox_all in data:
            try:
                new_order = order_service.generate_order(user, checkboxes, quantities, checkbox_all)
                updated_cart = new_order.cart
                self.assertTrue(updated_cart.is_archived)
                self.assertEqual(new_order.user, user)
            except errors.EmptyCartError as e:
                self.assertTrue(isinstance(e, errors.EmptyCartError))
