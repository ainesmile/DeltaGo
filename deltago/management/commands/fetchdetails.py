from django.core.management import BaseCommand
from deltago.models import BabyCare
from deltago.commodity_data.countdown import details
import json

class Command(BaseCommand):
    help = "Fetch product details"

    def handle(self, *args, **options):
        input_file = 'deltago/commodity_data/countdown/babycare.json'
        output_file = 'deltago/commodity_data/countdown/babycare_details.json'
        base_url = 'https://shop.countdown.co.nz'

        with open(input_file, 'r') as data_file:
            products = json.load(data_file)

        products_details = details.fetch(base_url, products)

        with open(output_file, 'w') as outfile:
            json.dump(products_details, outfile, indent=2)

