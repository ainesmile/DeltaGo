# -*- coding: utf-8 -*-
from deltago.models import Commodity

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

def sub(categ_name, sub_categ_name, page, per_page):
    categ, sub_categ = get_categs(categ_name, sub_categ_name)
    condition = {
        'category': categ,
        'sub_category': sub_categ
    }
    data = Commodity.objects.filter(**condition)
    products = pagination(data, page, per_page)
    empty_tips = "暂无商品，待上架。"
    return {
        "paginations": products,
        "products": products,
        "empty_tips": empty_tips
    }