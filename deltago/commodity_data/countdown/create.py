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

def create(item, fields, model):
    kwargs = set_kwargs(item, fields)
    new_record = model(**kwargs)
    new_record.save()

def save(items, fields, model):
    for item in items:
        create(item, fields, model)

def commodity(items):
    fields = ["name", "volume_size", "price", "was_price", "special_price",
        "category", "sub_category", "stockcode"]
    save(items, fields, Commodity)

def get_nutrition_details(nutrition_info):
    if nutrition_info:
        return (
            nutrition_info["nutritions"],
            nutrition_info["endorsements"],
            nutrition_info["ingredient"],
            nutrition_info["claims"]
        )
    else:
        return (None, None, None, None)