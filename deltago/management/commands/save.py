from django.core.management import BaseCommand
import json
from deltago.commodity_data.countdown.create import commodity, details, search

class Command(BaseCommand):
    help = 'Save data to database'

    def handle(self, *args, **options):
        with open('deltago/commodity_data/countdown/babycare.json') as babycare_data_file:
            babycare = json.load(babycare_data_file)
            
        with open('deltago/commodity_data/countdown/babycare_details.json') as babycare_details_data_file:
            babycare_details = json.load(babycare_details_data_file)
        
        commodity(babycare)
        details(babycare_details)
        search()