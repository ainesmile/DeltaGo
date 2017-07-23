# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
import json
from deltago.models import Commodity, Details

from .share import pagination

def get_categ(categ_name):
    categs = {
        "babycare": "B",
        "food": "F",
        "supplement": "P",
        "beauty": "U"
    }
    return categs[categ_name]

def get_sub_categ(categ_name, sub_categ_name):
    sub_categs = {
        'babycare': {
            'baby-food-from-4-mths': 'F4',
            'baby-food-from-6-mths': 'F6',
            'baby-food-from-9-mths': 'F9',
            'baby-food-from-12-mths': 'F12',
            'other-baby-foods': 'F',
            'medicinal-needs': 'M',
            'nappies-liners': 'N'
        },
        'supplement': {}
    }
    return sub_categs[categ_name][sub_categ_name]

def get_categs(categ_name, sub_categ_name):
    categ = get_categ(categ_name)
    sub_categ = get_sub_categ(categ_name, sub_categ_name)
    return (categ, sub_categ)

def get_sub_navs(categ_name):
    sub_navs = {
        "babycare" : [
            {
                "name": "baby-food-from-4-mths",
                "text": "辅食・4月+"
            },
            {
                "name": "baby-food-from-6-mths",
                "text": "辅食・6月+"
            },
            {
                "name": "baby-food-from-9-mths",
                "text": "辅食・9月+"
            },
            {
                "name": "baby-food-from-12-mths",
                "text": "辅食・12月+"
            },
            {
                "name": "other-baby-foods",
                "text": "辅食・其他"
            },
            {
                "name": "medicinal-needs",
                "text": "医疗"
            },
            {
                "name": "nappies-liners",
                "text": "纸尿布"
            }
        ]
    }
    return sub_navs[categ_name]

def sub(categ_name, sub_categ_name, page, per_page):
    categ, sub_categ = get_categs(categ_name, sub_categ_name)
    condition = {
        'category': categ,
        'sub_category': sub_categ
    }
    data = Commodity.objects.filter(**condition)
    products = pagination(data, page, per_page)
    empty_tips = "暂无商品，待上架。"
    sub_navs = get_sub_navs(categ_name)
    return {
        "paginations": products,
        "products": products,
        "empty_tips": empty_tips,
        "categ_name": categ_name,
        "sub_navs": sub_navs
    }

def json_loads(value):
    try:
        return json.loads(value)
    except TypeError:
        return None

def get_nutritions(nutrition):
    nutritions = json_loads(nutrition)
    results = []
    if nutritions:
        keys = ["Energy", "Protein", "Fat - Total", "Carbohydrate", "Sugars", "Sodium"]
        for index, key in enumerate(keys):
            n_index = index * 2
            item = (key, nutritions[n_index], nutritions[n_index+1])
            results.append(item)
    return results

def get_ingredients(ingredient):
    return json_loads(ingredient)

def get_details(product_id):
    try:
        product = Commodity.objects.get(pk=product_id)
        details = Details.objects.get(commodity=product)
        nutritions = get_nutritions(details.nutrition)
        ingredients = get_ingredients(details.ingredient)
        data = {
            "product": product,
            "details": details,
            "nutritions": nutritions,
            "ingredients": ingredients
        }
    except ObjectDoesNotExist:
        data = {}
    return data
