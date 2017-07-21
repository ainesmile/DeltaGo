# -*- coding: utf-8 -*-
from deltago.models import Commodity

from .share import pagination

def get_sub_nav(categ_name):
    sub_navs = {
        "B": {
            "F4": "辅食・4月+",
            "F6": "辅食・6月+",
            "F9": "辅食・9月+",
            "F12": "辅食・12月+",
            "F": "辅食・其他",
            "M": "医疗",
            "N": "纸尿布"
        },
        "P": {}
    }
    return sub_navs[categ_name]
    

def sub(condition, page, per_page):
    data = Commodity.objects.filter(**condition)
    products = pagination(data, page, per_page)
    empty_tips = "暂无商品，待上架。"
    sub_nav = get_sub_nav(condition["category"])

    return {
        "paginations": products,
        "products": products,
        "empty_tips": empty_tips,
        "sub_nav": sub_nav
    }
