from django.test import TestCase
from lxml import html
import requests
import re

from deltago.commodity_data.countdown import products

class ProductTest(TestCase):

    def setUp(self):
        with open('deltago/fixtures/commodity/countdown.py', 'r') as countdown:
            self.tree = html.fromstring(countdown.read())

        self.fields = {
            "name": {
                "ele": ".//span[@class=\"description span12 mspan8 \"]/text()",
                "need_process": 0
            },
            "volume_size": {
                "ele": ".//span[@class=\"volume-size\"]/text()",
                "need_process": 0
            },
            "price": {
                "ele": ".//span[@class=\"price din-medium\"]/text()[1]",
                "need_process": 1
            },
            "special_price": {
                "ele": ".//span[@class=\"price special-price din-medium savings-text\"]/text()[1]",
                "need_process": 1
            },
            "was_price": {
                "ele": ".//span[@class=\"was-price hidden-phone\"]/text()[1]",
                "need_process": 1
            }
        }
        self.category_field = {
            "category": "B",
            "sub_category": "F6"
        }
        self.stamp = "//div[@class=\"product-stamp product-stamp-grid \"]"
        self.product_elements = self.tree.xpath(self.stamp)
        self.product_element = self.product_elements[0]

    def test_replace(self):
        string = "    $2.49"
        s_expected = "$2.49"
        s_replaced = products.replace(string)
        self.assertEqual(s_replaced, s_expected)

    def test_field(self):
        data = [
            ("name", {"name": "Heinz Brekky Meal"}),
            ("price", {"price": "$2.49"}),
            ("was_price", {"was_price": "null"}),
        ]
        for f_name, f_result in data:
            f_details = self.fields[f_name]
            field = products.field(self.product_element, f_name, f_details)

    def test_product(self):
        expected = {
            "name": "Heinz Brekky Meal",
            "volume_size": "squeeze pouch 150g",
            "price": "$2.49",
            "special_price": "null",
            "was_price": "null"
        }
        expected.update(self.category_field)
        product = products.product(self.product_element, self.fields, self.category_field)
        self.assertEqual(product, expected)

    # def test_save(self):
    #     products.save('deltago/commodity_data/countdown/countdown.json', 'deltago/commodity_data/countdown/babycare.json')




