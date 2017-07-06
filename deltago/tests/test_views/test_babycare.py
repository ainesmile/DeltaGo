from django.test import TestCase, Client
from django.core.paginator import Page
from deltago.views.services.babycare import render_data, get_nutritions, get_ingredient, get_info
from deltago.models import BabyCareDetails

class BabyCareViewTest(TestCase):

    fixtures = [
        'deltago/fixtures/babycaredetails.json',
    ]

    def setUp(self):

        client = Client()
        response = client.get('babycare')
        self.request = response.wsgi_request
        self.details = BabyCareDetails.objects.get(stockcode="720986")

        self.expected_ingredient = "Pear1 (79%), Banana (14%), Blueberries (6%), Fruit Fibre, Vitamin C"
        self.expected_nutritions = [
            {'key': 'Energy', 'serving': '335kJ', 'gram': '280kJ'},
            {'key': 'Protein', 'serving': '0.6g', 'gram': '0.5g'},
            {'key': 'Fat - Total', 'serving': '0.2g', 'gram': '0.2g'},
            {'key': 'Carbohydrate', 'serving': '17.3g', 'gram': '14.4g'},
            {'key': 'Sugars', 'serving': '16.9g', 'gram': '14.1g'},
            {'key': 'Sodium', 'serving': '3mg', 'gram': '2mg'},
        ]

    def test_render_data(self):
        condition =  condition = {"sub_category": "F4"}
        page = self.request.GET.get('page', 1)
        data = render_data(condition, page, 20)
        self.assertTrue(isinstance(data["products"], Page))
        self.assertTrue(isinstance(data["paginations"], Page))

    def test_get_nutritions(self):
        nutrition = u'["335kJ", "280kJ", "0.6g", "0.5g", "0.2g", "0.2g", "17.3g", "14.4g", "16.9g", "14.1g", "3mg", "2mg"]'
        nutritions = get_nutritions(nutrition)
        self.assertEqual(nutritions, self.expected_nutritions)

    def test_get_ingredient(self):
        ingredient = u'{"note": "1 Organic", "text": "Pear1 (79%), Banana (14%), Blueberries (6%), Fruit Fibre, Vitamin C"}'
        text = get_ingredient(ingredient)
        self.assertEqual(text, self.expected_ingredient)

    def test_get_info(self):
        info = get_info(self.details)
        expected = {
            "ingredient": self.expected_ingredient,
            "nutritions": self.expected_nutritions
        }
        self.assertEqual(info, expected)
