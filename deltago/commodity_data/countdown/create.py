import json
from django.apps import apps
from deltago.models import Commodity, Details, Search

def set_kwargs(item, fields):
    kwargs = {}
    for field in fields:
        if item[field] == "null":
            kwargs[field] = None
        else:
            kwargs[field] = item[field]
    return kwargs