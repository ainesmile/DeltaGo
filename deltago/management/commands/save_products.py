from django.core.management import BaseCommand

import json
from deltago.models import Commodity, Details, Search
from deltago.management.commands._save_products_service import save_commodity_and_details, save_search

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        with open('deltago/commodity_data/product_list.json') as product_data_file:
            product_data = json.load(product_data_file)
        
        save_commodity_and_details(product_data)
        save_search()
