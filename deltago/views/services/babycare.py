# -*- coding: utf-8 -*-
import json
from deltago.models import BabyCare, BabyCareDetails
from .share import pagination

def render_data(condition, page, per_page):
    kwargs = condition.copy()
    products = BabyCare.objects.filter(**kwargs)
    result = pagination(products, page, per_page)
    empty_tips = "暂无商品，待上架。"
    return {
        "products": result,
        "paginations": result,
        "empty_tips": empty_tips
    }

def get_nutritions(nutrition):
    nutritions = []
    if nutrition and nutrition != "null":
        nutrition_list = json.loads(nutrition)
        keys = ["Energy", "Protein", "Fat - Total", "Carbohydrate", "Sugars", "Sodium"]
        for index, key in enumerate(keys):
            nutrition_index = index * 2
            serving = nutrition_list[nutrition_index]
            gram = nutrition_list[nutrition_index+1]
            item = {
                "key": key,
                "serving": serving,
                "gram": gram
            }
            nutritions.append(item)
    return nutritions

def get_ingredient(ingredient):
    if ingredient and ingredient != "null":
        return json.loads(ingredient)["text"]
    else:
        return None

def get_info(details):
    ingredient = details.ingredient
    if ingredient and ingredient != "null":
        return {
            "ingredient": get_ingredient(ingredient),
            "nutritions": get_nutritions(details.nutrition)
        }
    else:
        return None

def details_render_data(commodity_id):
    babycare = BabyCare.objects.get(pk=commodity_id)
    details = BabyCareDetails.objects.get(babycare=babycare)
    info = get_info(details)
    return {
        "product": babycare,
        "details": details,
        "info": info
    }
    
def month_category(month):
    category = {
        "4": "F4",
        "6": "F6",
        "9": "F9",
        "12": "F12"
    }
    return category[str(month)]