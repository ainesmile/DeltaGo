from django.test import TestCase
from deltago.templatetags import price

class PriceTagTest(TestCase):

    def test_human_price(self):
        data = [
            (1024, 10.24),
            ('', None)
        ]
        for p, e_result in data:
            result = price.human_price(p)
            self.assertEqual(result, e_result)