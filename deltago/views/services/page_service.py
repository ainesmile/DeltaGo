# -*- coding: utf-8 -*-

from deltago.views.services import share_service
from deltago.models import Commodity

def search_results(content, page, per_page):
    if content:
        results = Commodity.objects.filter(name__contains=content)
    else:
        results = []
    products = share_service.pagination(results, page, per_page)
    empty_tips = "暂无搜索结果，请尝试其他搜索关键词。"
    return {
        "paginations": products,
        "products": products,
        "empty_tips": empty_tips
    }