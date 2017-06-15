import json

# if __name__ == "__main__" and __package__ is None:
#     from os import sys, path
#     __package__ = "deltago.commodity_data.countdown"
#     sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from deltago.models.commodity import BabyCare


with open('deltago/commodity_data/countdown/babycare.json') as data_file:
    babycare_data = json.load(data_file)

def create_babycare(item):
    babycare = BabyCare(
        name = item["name"],
        volume_size = item["volume_size"],
        price = item["price"],
        was_price = item["was_price"],
        category = item["category"],
        sub_category = item["sub_category"]
    )
    babycare.save()

def babycare(babycare_data):
    map(lambda item: create_babycare(item), babycare_data)

# babycare(babycare_data)

# print len(babycare_data)
# babycare(babycare_data)
# babys = commodity.BabyCare.objects.all()
# print len(babys)

# if __name__ == '__main__' and __package__ is None:
#     from os import sys, path
#     sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

