from django.test import TestCase
from deltago.models.search import Search

from deltago.views.services import share

class PagesViewTest(TestCase):
    fixtures = [
        'deltago/fixtures/search.json',
        'deltago/fixtures/babycare.json',
        'deltago/fixtures/babycaredetails.json'
    ]

    def test_search(self):
        content = "Banana Avocado"
        expected = [2469]
        results = share.search_results(content)
        pks = []
        for r in results:
            pks.append(r.pk)
        self.assertEqual(pks, expected)