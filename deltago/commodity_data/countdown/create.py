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




# def babycare(babycare_data):
#     map(lambda item: create_babycare(item), babycare_data)

# babycare(babycare_data)

# print len(babycare_data)
# babycare(babycare_data)
# babys = commodity.BabyCare.objects.all()
# print len(babys)

# if __name__ == '__main__' and __package__ is None:
#     from os import sys, path
#     sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

