from django.test import TestCase
import json
from deltago.models import Commodity
from deltago.commodity_data.countdown import create

class CreateTest(TestCase):

    fixtures = [
        'deltago/fixtures/commodity.json',
    ]

    def setUp(self):
        with open('deltago/fixtures/commodity/commodity.json', 'r') as commodify_file:
            commodity_data = json.load(commodify_file)
        with open('deltago/fixtures/commodity/details.json', 'r') as details_file:
            details_data = json.load(details_file)

        self.items = commodity_data
        self.item = commodity_data[0]
        self.fields = ["name", "volume_size", "price", "was_price", "special_price",
        "category", "sub_category", "stockcode"]
        self.expected_kwargs ={
            "name": "commodity 11",
            "volume_size": "pouch 120g",
            "price": "2.09",
            "was_price": None,
            "special_price": None,
            "category": "B",
            "sub_category": "F4",
            "stockcode": "11",
        }

        self.details_item = details_data[0]
        self.nutrition_info = self.details_item["nutrition_info"]
        self.e_nutrition_details = (
            self.nutrition_info["nutritions"],
            self.nutrition_info["endorsements"],
            self.nutrition_info["ingredient"],
            self.nutrition_info["claims"]
        )

        self.commodity = Commodity.objects.get(pk=1)


    def test_set_kwargs(self):
        kwargs = create.set_kwargs(self.item, self.fields)
        self.assertEqual(kwargs, self.expected_kwargs)

    def test_create(self):
        create.create(self.item, self.fields, Commodity)
        new_commodity = Commodity.objects.get(stockcode="11")
        self.assertEqual(new_commodity.name, "commodity 11")

    def test_save(self):
        create.save(self.items, self.fields, Commodity)
        new_commodity_11 = Commodity.objects.get(stockcode="11")
        new_commodity_12 = Commodity.objects.get(stockcode="12")
        self.assertEqual(new_commodity_11.name, "commodity 11")
        self.assertEqual(new_commodity_12.name, "commodity 12")
        self.assertEqual(Commodity.objects.count(), 12)

    def test_get_nutrition_details(self):
        results = create.get_nutrition_details(self.nutrition_info)
        self.assertEqual(results, self.e_nutrition_details)
        