from django.test import TestCase
from lxml import html
from deltago.commodity_data.countdown import details


class DetailsTest(TestCase):
    def setUp(self):

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

    def test_get_urls(self):
        expected = {
            "Heinz Organic Baby Food Apple, Banana Avocado": "https://shop.countdown.co.nz/Shop/ProductDetails?stockcode=757788&name=heinz-organic-baby-food-apple-banana-avocado",
            "Heinz Organic Baby Food Apple,raspbry, Blackbry": "https://shop.countdown.co.nz/Shop/ProductDetails?stockcode=757815&name=heinz-organic-baby-food-appleraspbry-blackbry",
            "Natureland Baby Food Sherperds Pie & Mash": "https://shop.countdown.co.nz/Shop/ProductDetails?stockcode=341710&name=natureland-baby-food-sherperds-pie-mash",
            "Natureland Baby Food Vanilla Custard": "https://shop.countdown.co.nz/Shop/ProductDetails?stockcode=341713&name=natureland-baby-food-vanilla-custard"
        }

        urls = details.get_urls(self.base_url, self.products)
        self.assertEqual(urls, expected)

