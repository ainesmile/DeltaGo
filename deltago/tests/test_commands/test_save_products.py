from django.test import TestCase
import json
from deltago.models import Commodity, Details, Search
from deltago.management.commands import _save_products_service

class SaveProductsServiceTest(TestCase):
    fixtures = []

    def setUp(self):
        with open('deltago/commodity_data/product_list.json') as product_data_file:
            product_data = json.load(product_data_file)

        self.items = product_data
        self.item = product_data[0]
        self.name = "Pic's Peanut Butter Crunchy No Salt 380g"

    def test_set_kwargs(self):
        fields = ["name", "price", "field_does_not_exit"]

        e_kwargs = {
            "name": self.name,
            "price": 650,
            "field_does_not_exit": None
        }


        kwargs = _save_products_service.set_kwargs(self.item, fields)
        self.assertEqual(kwargs, e_kwargs)

    def test_create(self):
        commodity_fields = ["name", "price", "special_price", "volume_size", "category"]
        new_commodity = _save_products_service.create(self.item, commodity_fields, Commodity)
        self.assertEqual(new_commodity.name, self.name)
        self.assertEqual(new_commodity.price, 650)

    def test_save_commodity_and_details(self):
        _save_products_service.save_commodity_and_details(self.items)
        commodity_details = Details.objects.all()
        commodities = Commodity.objects.all()
        self.assertEqual(commodity_details.count(), commodities.count())
        for details in commodity_details:
            self.assertIn(details.commodity, commodities)

    def test_save_search(self):
        _save_products_service.save_search()
        commodities = Commodity.objects.all()
        searches = Search.objects.all()
        self.assertEqual(commodities.count(), searches.count())
        for search in searches:
            self.assertIn(search.commodity, commodities)