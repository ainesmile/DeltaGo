from django.core.management import BaseCommand
from deltago.commodity_data.countdown import products


class Command(BaseCommand):
    help = 'fetch data from countdown and then save them to file as json'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str)
        parser.add_argument('output_file', type=str)

    def handle(self, *args, **options):
        input_file = options["input_file"]
        output_file = options["output_file"]
        # input_file = 'deltago/commodity_data/countdown/countdown.json'
        # output_file = 'deltago/commodity_data/countdown/babycare.json'
        products.save(input_file, output_file)