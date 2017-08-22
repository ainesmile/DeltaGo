import json
from django.apps import apps
from deltago.models import Commodity, Details, Search

def set_kwargs(item, fields):
    kwargs = {}
    for field in fields:
        try:
            value = item[field]
            if value == "null":
                value = None
        except:
            value = None
        kwargs[field] = value
    return kwargs

def create(item, fields, model):
    kwargs = set_kwargs(item, fields)
    new_record = model(**kwargs)
    new_record.save()
    return new_record

def save_commodity_and_details(items):
    commodity_fields = ["name", "price", "special_price", "volume_size", "category"]
    details_fields = ["commodity", "weight", "ingredient", "serving_size", "servings", "nutritions", "claims",
        "health_star_rating", "made_in", "pic_url", "description", "endorsement"]
    for item in items:
        new_commodity = create(item, commodity_fields, Commodity)
        item["commodity"] = new_commodity
        create(item, details_fields, Details)

def save_search():
    commodities = Commodity.objects.all()
    for commodity in commodities:
        kwargs = {
            "name": commodity.name,
            "commodity": commodity,
        }
        new_search = Search(**kwargs)
        new_search.save()