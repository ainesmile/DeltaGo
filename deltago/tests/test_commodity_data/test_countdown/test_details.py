from django.test import TestCase
from lxml import html
from deltago.commodity_data.countdown import details


class DetailsTest(TestCase):
    def setUp(self):
        with open('deltago/fixtures/commodity/details.py', 'r') as data_file:
            self.tree = html.fromstring(data_file.read())

        self.base_url = 'https://shop.countdown.co.nz'
        self.products = [
            {
                "category": "B", 
                "volume_size": "pouch 120g", 
                "href": "/Shop/ProductDetails?stockcode=757788&name=heinz-organic-baby-food-apple-banana-avocado", 
                "was_price": "null", 
                "sub_category": "F4", 
                "price": "2.09", 
                "special_price": "null", 
                "name": "Heinz Organic Baby Food Apple, Banana Avocado"
            }, 
            {
                "category": "B", 
                "volume_size": "pouch 120g", 
                "href": "/Shop/ProductDetails?stockcode=757815&name=heinz-organic-baby-food-appleraspbry-blackbry", 
                "was_price": "null", 
                "sub_category": "F4", 
                "price": "2.09", 
                "special_price": "null", 
                "name": "Heinz Organic Baby Food Apple,raspbry, Blackbry"
            },
            {
                "category": "B", 
                "volume_size": "120g", 
                "href": "/Shop/ProductDetails?stockcode=341710&name=natureland-baby-food-sherperds-pie-mash", 
                "was_price": "null", 
                "sub_category": "F6", 
                "price": "1.80", 
                "special_price": "null", 
                "name": "Natureland Baby Food Sherperds Pie & Mash"
            }, 
            {
                "category": "B", 
                "volume_size": "pouch 120g", 
                "href": "/Shop/ProductDetails?stockcode=341713&name=natureland-baby-food-vanilla-custard", 
                "was_price": "null", 
                "sub_category": "F6", 
                "price": "1.80", 
                "special_price": "null", 
                "name": "Natureland Baby Food Vanilla Custard"
            }
        ]
        self.element = ".//div[@class=\"product-details-description\"]"
        self.field_name = ".//div[@class=\"navigation-toggle-children\"]/p/text()"
        self.details_item = self.tree.xpath(self.element)[0]

    def test_get_ingredient_text(self):
        expected = "Apples1 (89%), Raspberries (7%), Blackberries (4%)"
        text = details.get_ingredient_text(self.details_item)
        self.assertEqual(text, expected)

    def test_get_ingredient_note(self):
        expected = "1 Organic"
        note = details.get_ingredient_note(element)
        self.assertEqual(note, expected)

    def test_get_origin(self):
        expected = "Made in Australia from imported and local ingredients"
        origin = details.get_origin(self.tree)
        self.assertEqual(origin, expected)

    def test_get_urls(self):
        expected = {
            "Heinz Organic Baby Food Apple, Banana Avocado": "https://shop.countdown.co.nz/Shop/ProductDetails?stockcode=757788&name=heinz-organic-baby-food-apple-banana-avocado",
            "Heinz Organic Baby Food Apple,raspbry, Blackbry": "https://shop.countdown.co.nz/Shop/ProductDetails?stockcode=757815&name=heinz-organic-baby-food-appleraspbry-blackbry",
            "Natureland Baby Food Sherperds Pie & Mash": "https://shop.countdown.co.nz/Shop/ProductDetails?stockcode=341710&name=natureland-baby-food-sherperds-pie-mash",
            "Natureland Baby Food Vanilla Custard": "https://shop.countdown.co.nz/Shop/ProductDetails?stockcode=341713&name=natureland-baby-food-vanilla-custard"
        }

        urls = details.get_urls(self.base_url, self.products)
        self.assertEqual(urls, expected)