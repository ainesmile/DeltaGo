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
            {'key': 'Energy', 'serving': '320kJ', 'gram': '265kJ'},
            {'key': 'Protein', 'serving': '2g', 'gram': '1.7g'},
            {'key': 'Fat - Total', 'serving': '0.1g', 'gram': '0.1g'},
            {'key': 'Carbohydrate', 'serving': '15.7g', 'gram': '13.1g'},
            {'key': 'Sugars', 'serving': '10.9g', 'gram': '9.1g'},
            {'key': 'Sodium', 'serving': '2mg', 'gram': '1mg'},
        ]


    def test_render_data(self):
        condition =  condition = {"sub_category": "F4"}
        page = self.request.GET.get('page', 1)
        data = render_data(condition, page, 20)
        self.assertTrue(isinstance(data["products"], Page))
        self.assertTrue(isinstance(data["paginations"], Page))

    def test_get_nutritions(self):
        nutrition = "[\"320kJ\", \"265kJ\", \"2g\", \"1.7g\", \"0.1g\", \"0.1g\", \"15.7g\", \"13.1g\", \"10.9g\", \"9.1g\", \"2mg\", \"1mg\", \"8mg\", \"25%\", \"7mg\"]"
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
