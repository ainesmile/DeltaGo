from django.test import TestCase
import json
from deltago.models import Commodity
from deltago.commodity_data.countdown import create

class CreateTest(TestCase):

    def setUp(self):
        with open('deltago/fixtures/commodity/commodity.json', 'r') as data_file:
            commodity_data = json.load(data_file)

        self.items = commodity_data
        self.item = commodity_data[0]
        self.fields = ["name", "volume_size", "price", "was_price", "special_price",
        "category", "sub_category", "stockcode"]
        self.expected_kwargs ={
            "name": "commodity 1",
            "volume_size": "pouch 120g",
            "price": "2.09",
            "was_price": None,
            "special_price": None,
            "category": "B",
            "sub_category": "F4",
            "stockcode": "11",
        }


    def test_set_kwargs(self):
        kwargs = create.set_kwargs(self.item, self.fields)
        self.assertEqual(kwargs, self.expected_kwargs)