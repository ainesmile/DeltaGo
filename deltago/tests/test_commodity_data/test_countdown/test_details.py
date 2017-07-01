from django.test import TestCase
from lxml import html
import requests
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
        self.element_name = ".//div[@class=\"product-details-description\"]"
        self.field_name = ".//div[@class=\"navigation-toggle-children\"]/p/text()"
        self.ingredients = self.tree.xpath(self.element_name)[0]
        self.nutritional = self.tree.xpath(self.element_name)[1]
        self.claims = self.tree.xpath(self.element_name)[2]

        self.expected_claims = "No Added Colours or Flavours, No Preservatives, No Added Sugar"
        self.expected_nutritions = ['335kJ', '280kJ', '0.6g', '0.5g', '0.2g', '0.2g', '17.3g', '14.4g', '16.9g', '14.1g', '3mg', '2mg']
        self.expected_ingredient = {
            "text": "Apples1 (89%), Raspberries (7%), Blackberries (4%)",
            "note": "1 Organic"
        }
        self.expected_endorsements = "Australian Certified Organic"
        self.expected_origin = "Made in Australia from imported and local ingredients"
        self.expected_descriptions = {
            "ingredient": self.expected_ingredient,
            "nutritions": self.expected_nutritions,
            "claims": self.expected_claims,
            "endorsements": self.expected_endorsements
        }

    def test_get_origin(self):
        origin = details.get_origin(self.tree)
        self.assertEqual(origin, self.expected_origin)

    def test_get_node_value(self):
        node_value = details.get_node_value(self.claims, self.field_name)
        self.assertEqual(node_value, self.expected_claims)

    def test_get_ingredient(self):
        ingredient = details.get_ingredient(self.ingredients)
        self.assertEqual(ingredient, self.expected_ingredient)

    def test_get_nutritions(self):
        nutritions = details.get_nutritions(self.nutritional)
        self.assertEqual(nutritions, self.expected_nutritions)

    def test_get_descriptions(self):
        descriptions = details.get_descriptions(self.tree)
        self.assertEqual(descriptions, self.expected_descriptions)

    # def test_get_details(self):
    #     product_details = details.get_details(self.base_url, self.product)
    #     self.assertEqual(product_details, self.expected_details)
