from django.core.management import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Clear the specified table'

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str)

    def handle(self, *args, **options):
        model_name = options["model_name"]
        try:
            table = apps.get_model(app_label='deltago', model_name=model_name)
            table.objects.all().delete()
            if len(table.objects.all()) == 0:
                print model_name, "clear success."
            else:
                print "Clear failed."
        except LookupError as e:
            print e
        
