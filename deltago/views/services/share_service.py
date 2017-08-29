from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from deltago.models import Details, Commodity

def pagination(items, page, paginate_by):
    paginator = Paginator(items, paginate_by)
    try:
        text = paginator.page(page)
    except PageNotAnInteger:
        text = paginator.page(1)
    except EmptyPage:
        text = paginator.page(paginator.num_pages)
    return text

def cal_ship_fee(cartships):
    fee_per_kg = 500
    cal_kg = 1000
    box_weight = 200
    total_weight = 0
    for cartship in cartships:
        product = cartship.commodity
        details = Details.objects.get(commodity=product)
        weight = details.weight
        quantity = cartship.quantity
        product_weight = weight * quantity
        total_weight += product_weight

    total_weight += box_weight
    cal_weight = max(float(total_weight)/cal_kg, 1.00)
    return round(fee_per_kg * cal_weight, 2)


def get_cartship_subtotal(cartship):
    commodity = cartship.commodity
    price = commodity.price
    quantity = cartship.quantity
    return price * quantity

def get_cartships_subtotal(cartships):
    subtotal = 0
    for cartship in cartships:
        subtotal += get_cartship_subtotal(cartship)
    return subtotal

