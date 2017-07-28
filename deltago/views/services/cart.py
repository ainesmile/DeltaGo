# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from deltago.models import Commodity, Cart, Cartship
from deltago.views.services.share import pagination

def user_current_cart(user):
    try:
        cart = Cart.objects.get(user=user, is_archived=False)
    except ObjectDoesNotExist:
        cart = Cart(user=user)
        cart.save()
    return cart

def get_commodity(product_id):
    try:
        commodity = Commodity.objects.get(pk=product_id)
        return commodity
    except ObjectDoesNotExist:
        return None

def create_cartship(commodity, cart, quantity):
    new_cartship = Cartship(
        commodity=commodity,
        cart=cart,
        quantity=quantity)
    new_cartship.save()
    return new_cartship

def update_cartship_quantity(cartship, quantity):
    cartship.quantity += quantity
    cartship.updated_date = timezone.now()
    cartship.save()
    return cartship

def update_or_create_cartship(cart, commodity, quantity):
    try:
        cartship = Cartship.objects.get(cart=cart, commodity=commodity)
        return update_cartship_quantity(cartship, quantity)
    except ObjectDoesNotExist:
        return create_cartship(commodity, cart, quantity)

def add_to_cart(user, product_id, quantity):
    cart = user_current_cart(user)
    commodity = get_commodity(product_id)
    if not commodity:
        return None
    else:
        return update_or_create_cartship(cart, commodity, quantity)

def cartship_list(user, page, per_page):
    cart = user_current_cart(user)
    data = Cartship.objects.filter(cart=cart)
    cartshipes = pagination(data, page, per_page)
    empty_tips = "购物车空啦"
    return {
        "cartshipes": cartshipes,
        "paginations": cartshipes,
        "empty_tips": empty_tips
    }
