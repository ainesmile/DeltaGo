from deltago.models import BabyCare
from .share import pagination

def render_data(condition, page, per_page):
    kwargs = condition.copy()
    products = BabyCare.objects.filter(**kwargs)
    result = pagination(products, page, per_page)
    return {
        "products": result,
        "paginations": result
    }