import json
from deltago.models.commodity import BabyCare, BabyCareDetails

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

def create_babycare(item):
    name = item["name"]
    try:
        details = BabyCareDetails.objects.filter(name=name)[0]
    except IndexError:
        return None
    babycare = BabyCare(
        name = item["name"],
        volume_size = item["volume_size"],
        price = item["price"],
        was_price = item["was_price"],
        category = item["category"],
        sub_category = item["sub_category"],
        details = details
    )
    babycare.save()
