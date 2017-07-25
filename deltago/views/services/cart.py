# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist

from deltago.models import Commodity, Cart
from deltago.views.services.share import pagination

def create_cart(commodity, quantity):
    new_cart = Cart(
        commodity = commodity,
        quantity = quantity
        )
    new_cart.save()
    return new_cart

def update_cart(cart, quantity):
    cart.quantity += quantity
    cart.save()

def add_to_cart(product_id, quantity):
    try:
        commodity = Commodity.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        return None
    try:
        cart = Cart.objects.get(commodity=commodity)
        update_cart(cart, quantity)
    except ObjectDoesNotExist:
        cart = create_cart(commodity, quantity)
    return cart


def cart_list(page, per_page):
    data = Cart.objects.all()
    carts = pagination(data, page, per_page)
    empty_tips = "购物车空啦"
    return {
        "carts": carts,
        "paginations": carts,
        "empty_tips": empty_tips
    }
