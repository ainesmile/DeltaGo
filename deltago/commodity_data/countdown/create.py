import json
from deltago.models.commodity import BabyCare, BabyCareDetails
from deltago.models.search import Search

def create_babycare_details(item):
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
        stockcode = item["stockcode"],
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
    for item in items:
        create_babycare_details(item)

def filter_details(stockcode):
    try:
        details = BabyCareDetails.objects.filter(stockcode=stockcode)[0]
        return details
    except IndexError:
        return None

def create_babycare(item):
    stockcode = item["stockcode"]
    details = filter_details(stockcode)
    babycare = BabyCare(
        stockcode = stockcode,
        name = item["name"],
        volume_size = item["volume_size"],
        price = item["price"],
        was_price = item["was_price"],
        special_price = item["special_price"],
        category = item["category"],
        sub_category = item["sub_category"],
        details = details
    )
    babycare.save()

def save_babycare(items):
    for item in items:
        create_babycare(item)

def get_model_name(category):
    model_names = {
        'B': 'BabyCare',
        'F': 'Food',
        'P': 'Supplement',
        'U': 'Beauty',
        'S': 'Special'
    }
    return model_names[category]

def create_search(item):
    model_name = get_model_name(item["category"])
    new_search = Search(
        name = item["name"],
        stockcode = item["stockcode"],
        model_name = model_name)
    new_search.save()

def save_search(items):
    for item in items:
        create_search(item)

