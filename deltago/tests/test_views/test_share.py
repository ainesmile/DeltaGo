from django.test import TestCase
from deltago.models.search import Search
from deltago.models import BabyCare

from deltago.views.services import share

class ShareSerivcesTest(TestCase):
    fixtures = [
        'deltago/fixtures/search.json',
        'deltago/fixtures/babycare.json',
        'deltago/fixtures/babycaredetails.json'
    ]

    def test_search_results(self):
        content = "Banana Avocado"
        expected = [2469]
        results = share.search_results(content)
        pks = []
        for r in results:
            pks.append(r.pk)
        self.assertEqual(pks, expected)

    def test_get_model(self):
        category = 'B'
        model_name = share.get_model(category)
        self.assertEqual(model_name, BabyCare)