from django.test import TestCase
import json
from deltago.models import Commodity, Details, Search
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

        self.details_items = details_data
        self.details_item = details_data[0]
        self.nutrition_info = self.details_item["nutrition_info"]
        self.e_nutrition_details = (
            json.dumps(self.nutrition_info["nutritions"]),
            self.nutrition_info["endorsements"],
            json.dumps(self.nutrition_info["ingredient"]),
            self.nutrition_info["claims"]
        )

        self.commodity = Commodity.objects.get(pk=1)

        self.e_details_item = {
            "commodity": self.commodity,
            "description": self.details_item["descriptions"],
            "pic_url": self.details_item["pic_url"],
            "ingredient": json.dumps(self.details_item["nutrition_info"]["ingredient"]),
            "claim": self.details_item["nutrition_info"]["claims"],
            "endorsement": self.details_item["nutrition_info"]["endorsements"],
            "nutrition": json.dumps(self.details_item["nutrition_info"]["nutritions"])
        }


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

    def test_get_details_item(self):
        item = create.get_details_item(self.details_item, self.commodity)
        self.assertEqual(item, self.e_details_item)

    def test_get_details_items(self):
        items = create.get_details_items(self.details_items)
        self.assertEqual(items, [self.e_details_item])

    def test_details(self):
        create.details(self.details_items)
        self.assertEqual(Details.objects.count(), 1)

    def test_search(self):
        create.search()
        searches = Search.objects.all()
        commodities = Commodity.objects.all()
        for index, search in enumerate(searches):
            commodity = commodities[index]
            self.assertEqual(search.name, commodity.name)
            self.assertEqual(search.commodity, commodity)


