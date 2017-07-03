from django.core.management import BaseCommand
import json
from deltago.commodity_data.countdown import create

class Command(BaseCommand):
    help = 'Save commodity data to datebase'

    # def add_arguments(self, parser):
    #     parser.add_argument('input_file', type=str)

    def handle(self, *args, **options):
        # input_file = options["input_file"]

        with open('deltago/commodity_data/countdown/babycare_details.json') as data_file:
            data = json.load(data_file)

            for d in data:
                create.create_babycare_details(d)

