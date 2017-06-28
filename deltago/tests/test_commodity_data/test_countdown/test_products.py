from django.test import TestCase
from lxml import html
import requests
import re
import json
import HTMLParser


from deltago.commodity_data.countdown import products

class ProductTest(TestCase):

    def setUp(self):
        with open('deltago/fixtures/commodity/countdown.py', 'r') as countdown:
            self.tree = html.fromstring(countdown.read())

        with open('deltago/fixtures/commodity/babycare.py', 'r') as babycare:
            self.intact_tree = html.fromstring(babycare.read())

        with open('deltago/commodity_data/countdown/countdown.json', 'r') as data_file:
            data = json.load(data_file)
            self.fields = data["fields"]
            self.stamp = data["stamp"]

        self.category_field = {
            "category": "B",
            "sub_category": "F6"
        }
        self.product_elements = self.tree.xpath(self.stamp)
        self.product_element = self.product_elements[0]

    def test_replace(self):
        data = [
            ('    $2.49', '2.49'),
            ('was    $1.2', '1.2'),
            ('was    $1.00', '1.00')
        ]
        for str, result in data:
            self.assertEqual(products.replace(str), result)

    def test_page_number(self):
        element = ".//div[@class=\"paging-description hidden-tablet \"]/text()"
        data = [
            (2, 14),
            (3, 10),
            (4, 7),
        ]
        for per, page_expected in data:
            page = products.page_number(self.intact_tree, element, per)
            self.assertEqual(page_expected, page)


    def test_field(self):
        data = [
            ("name", {"name": "Heinz Brekky To Go Kids Meal Banana Oats Cinnamon"}),
            ("price", {"price": "$2.49"}),
            ("was_price", {"was_price": "null"}),
        ]
        for f_name, f_result in data:
            f_details = self.fields[f_name]
            field = products.field(self.product_element, f_name, f_details)

    def test_product(self):
        expected = {
            "href": "/Shop/ProductDetails?stockcode=790503&amp;name=heinz-brekky-to-go-kids-meal-banana-oats-cinnamon",
            "was_price": "null",
            "special_price": "null",
            "price": "$2.49",
            "volume_size": "squeeze pouch 150g",
            "name": "Heinz Brekky To Go Kids Meal Banana Oats Cinnamon"
        }
        expected.update(self.category_field.copy())
        expected_href = HTMLParser.HTMLParser().unescape(expected["href"])

        product = products.product(
            self.product_element,
            self.fields,
            self.category_field
        )

        self.assertEqual(product["href"], expected_href)
        self.assertEqual(product["was_price"], expected["was_price"])
        self.assertEqual(product["special_price"], expected["special_price"])
        self.assertEqual(product["volume_size"], expected["volume_size"])
        self.assertEqual(product["name"], expected["name"])

    # def test_save(self):
    #     products.save('deltago/commodity_data/countdown/countdown.json', 'deltago/commodity_data/countdown/babycare.json')




