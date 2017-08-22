from django.test import TestCase
import json
from deltago.models import Commodity, Details
from deltago.views.services import product_service

class ProductsViewTest(TestCase):
    fixtures = [
        'deltago/fixtures/products.json',
        'deltago/fixtures/details.json',
    ]

    def setUp(self):
        self.product = Commodity.objects.get(pk=1)
        self.details = Details.objects.get(pk=1)
        self.nutritions = u'[["Energy", "370.5kJ", "2470kJ"], ["Protein", "4.6g", "30.3g"]]'
        self.e_nutritions = [
            (u'Energy', u'370.5kJ', u'2470kJ'),
            (u'Protein', u'4.6g', u'30.3g')
        ]

    def test_get_nutritions(self):
        result = product_service.get_nutritions(self.nutritions)
        self.assertEqual(result, self.e_nutritions)


        