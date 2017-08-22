from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import json
from deltago.models import Commodity, Details
from deltago.views.services import share_service

def products(page, per_page):
    commodities = Commodity.objects.all()
    paginations = share_service.pagination(commodities, page, per_page)
    return {
        "products": paginations,
        "paginations": paginations,
    }

def details(commodity_id):
    try:
        commodity = Commodity.objects.get(pk=commodity_id)
        product_details = Details.objects.get(commodity=commodity)
        product_details.nutrition_table = get_nutritions(product_details.nutritions)
        product_details.health_star_list = range(product_details.health_star_rating)
    except ObjectDoesNotExist:
        raise Http404()
    return {"details": product_details}

def get_nutritions(nutritions):
    result = []
    j_nutritions = json.loads(nutritions)
    for nutrition_item in j_nutritions:
        result.append(tuple(nutrition_item))
    return result
    