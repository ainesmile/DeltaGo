from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(items, page, paginate_by):
    paginator = Paginator(items, paginate_by)
    try:
        text = paginator.page(page)
    except PageNotAnInteger:
        text = paginator.page(1)
    except EmptyPage:
        text = paginator.page(paginator.num_pages)
    return text

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

