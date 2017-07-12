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
        self.details = BabyCareDetails.objects.get(pk=1)
        self.expected_ingredient = "Apples1 (81%), Banana (13.7%), Avocado (5%), Vitamin C"
        self.expected_nutritions = [
            {'key': 'Energy', 'serving': '385kJ', 'gram': '320kJ'},
            {'key': 'Protein', 'serving': '0.7g', 'gram': '0.6g'},
            {'key': 'Fat - Total', 'serving': '1.4g', 'gram': '1.2g'},
            {'key': 'Carbohydrate', 'serving': '17.8g', 'gram': '14.8g'},
            {'key': 'Sugars', 'serving': '16.9g', 'gram': '14.1g'},
            {'key': 'Sodium', 'serving': '3mg', 'gram': '2mg'},
        ]
        self.nutrition = u'[\"385kJ\", \"320kJ\", \"0.7g\", \"0.6g\", \"1.4g\", \"1.2g\", \"17.8g\", \"14.8g\", \"16.9g\", \"14.1g\", \"3mg\", \"2mg\"]'
        self.ingredient = u'{\"note\": \"1 Organic\", \"text\": \"Apples1 (81%), Banana (13.7%), Avocado (5%), Vitamin C\"}'

    def test_render_data(self):
        condition =  condition = {"sub_category": "F4"}
        page = self.request.GET.get('page', 1)
        data = render_data(condition, page, 20)
        self.assertTrue(isinstance(data["products"], Page))
        self.assertTrue(isinstance(data["paginations"], Page))

    def test_get_nutritions(self):
        nutritions = get_nutritions(self.nutrition)
        self.assertEqual(nutritions, self.expected_nutritions)

    def test_get_ingredient(self):
        text = get_ingredient(self.ingredient)
        self.assertEqual(text, self.expected_ingredient)

    def test_get_info(self):
        info = get_info(self.details)
        expected = {
            "ingredient": self.expected_ingredient,
            "nutritions": self.expected_nutritions
        }
        self.assertEqual(info, expected)
