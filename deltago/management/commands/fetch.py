from django.core.management import BaseCommand
import json
from deltago.commodity_data.countdown import products


class Command(BaseCommand):
    help = 'fetch data from countdown and then save them to file as json'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)
        parser.add_argument('output_file', type=str)

    def handle(self, *args, **options):
        input_file = 'deltago/commodity_data/countdown/countdown.json'
        
        # BabyCare category is "B"
        # output_file = 'deltago/commodity_data/countdown/babycare.json'
        category = options["category"]
        output_file = options["output_file"]

        with open(input_file, 'r') as input_data_file:
            data = json.load(input_data_file)
            countdown = data["countdown"]
            category_data = countdown[category]
            fields = data["fields"]
            stamp = data["stamp"]
            items_number_element = data["items_number_element"]
            per_page = data["per_page"]

        product_list = products.sub(category, category_data, fields, stamp, items_number_element, per_page)

        with open(output_file, 'w') as output_data_file:
            json.dump(products, output_data_file, indent=2)