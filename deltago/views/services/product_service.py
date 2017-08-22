from deltago.models import Commodity
from deltago.views.services import share_service

def products(page, per_page):
    commodities = Commodity.objects.all()
    paginations = share_service.pagination(commodities, page, per_page)
    return {
        "products": paginations,
        "paginations": paginations,
    }