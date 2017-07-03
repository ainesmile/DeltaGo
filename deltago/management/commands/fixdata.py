from django.core.management import BaseCommand
import json
from deltago.commodity_data.countdown import details

class Command(BaseCommand):
    help = 'add detail item to product details'

    def handle(self, *args, **options):

        product_file = 'deltago/commodity_data/countdown/babycare.json'
        details_file = 'deltago/commodity_data/countdown/babycare_details.json'

        with open(product_file, 'r') as product_data_file:
            products_data = json.load(product_data_file)

        with open(details_file, 'r') as details_data_file:
            details_data = json.load(details_data_file)


        stockcode_set = set()

        for index, product in enumerate(products_data):

            href = product["href"]
            stockcode = details.get_stockcode(href)
            product["stockcode"] = stockcode

            detail = details_data[index]
            detail["stockcode"] = stockcode
            
            if stockcode not in stockcode_set:
                stockcode_set.add(stockcode)
            else:
                print "stockcode is not unique"


        with open(product_file, 'w') as product_output_file:
            json.dump(products_data, product_output_file, indent=2)

        with open(details_file, 'w') as details_file_output_file:
            json.dump(details_data, details_file_output_file, indent=2)