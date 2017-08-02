from django.test import TestCase
from datetime import datetime

from deltago.templatetags import date

class DateTagTest(TestCase):

    def setUp(self):
        self.value = datetime(2017, 7, 30, 10, 55, 01, 479644)
        self.e_date = '2017-07-30'
        self.e_hour = '10:55:01'


    def test_padding_date(self):
        data = [
            (1, '01'),
            (10, '10')
        ]
        for value, e_result in data:
            result = date.padding_date(value)
            self.assertEqual(result, e_result)

    def test_postfix_date(self):
        data = [
            (2017, '-'),
            (7, '-'),
            (30, '')
        ]
        result = date.postfix_date(data)
        self.assertEqual(result, self.e_date)

    def test_human_time_date(self):
        result = date.human_time_date(self.value)
        self.assertEqual(result, self.e_date)
        
    def test_human_time_hour(self):
        result = date.human_time_hour(self.value)
        self.assertEqual(result, self.e_hour)
