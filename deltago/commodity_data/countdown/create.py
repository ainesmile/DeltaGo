import json
from django.apps import apps
from deltago.models.commodity import BabyCare, BabyCareDetails
from deltago.models.search import Search

def create_babycare(item):
    babycare = BabyCare(
        stockcode = item["stockcode"],
        name = item["name"],
        volume_size = item["volume_size"],
        price = item["price"],
        was_price = item["was_price"],
        special_price = item["special_price"],
        category = item["category"],
        sub_category = item["sub_category"],
    )
    babycare.save()

def save_babycare(items):
    for item in items:
        create_babycare(item)


def create_babycare_details(item, babycare):
    nutrition_info = item["nutrition_info"]
    if nutrition_info:
        nutrition = nutrition_info["nutritions"]
        ingredient = nutrition_info["ingredient"]
        claim = nutrition_info["claims"]
        endorsement = nutrition_info["endorsements"]
    else:
        nutrition = None
        ingredient = None
        claim = None
        endorsement = None

    details = BabyCareDetails(
        babycare = babycare,
        name = item["name"],
        description = item["descriptions"],
        pic_url = item["pic_url"],
        nutrition = json.dumps(nutrition),
        ingredient = json.dumps(ingredient),
        claim = claim,
        endorsement = endorsement
    )
    details.save()

def save_details(items):
    babycares = BabyCare.objects.all()
    for index, babycare in enumerate(babycares):
        stockcode = babycare.stockcode
        item =items[index]
        if item["stockcode"] == stockcode:
            create_babycare_details(item, babycare)
        else:
            print item["stockcode"], stockcode
            print 'BabyCare and BabyCareDetails do not match'

def create_search(name, pk, model_name):
    new_search = Search(
        name = name,
        commodity_id = pk,
        model_name = model_name)
    new_search.save()

def save_search(model_name):
    model = apps.get_model(app_label='deltago', model_name=model_name)
    objects = model.objects.all()
    for object in objects:
        create_search(object.name, object.pk, model_name)