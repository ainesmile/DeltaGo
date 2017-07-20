import json
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
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

def get_details_item(item, commodity):
    data = {}
    data["commodity"] = commodity
    data["description"] = item["descriptions"] or None
    data["pic_url"] = item["pic_url"] or None
    nutrition_info = item["nutrition_info"]
    data["nutrition"], data["endorsement"], \
        data["ingredient"], data["claim"] = get_nutrition_details(nutrition_info)
    return data

def get_details_items(items):
    new_items = []
    for item in items:
        try:
            commodity = Commodity.objects.get(stockcode=item["stockcode"])
            new_item = get_details_item(item, commodity)
        except ObjectDoesNotExist:
            new_item = None
        if new_item:
            new_items.append(new_item)
    return new_items

def details(items):
    fields = ["commodity", "pic_url", "description",
        "nutrition", "ingredient", "claim", "endorsement"]
    new_items = get_details_items(items)
    save(new_items, fields, Details)

def search():
    commodities = Commodity.objects.all()
    for commodity in commodities:
        kwargs = {
            "name": commodity.name,
            "commodity": commodity,
        }
        new_search = Search(**kwargs)
        new_search.save()
