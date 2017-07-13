# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.apps import apps
import copy
from .share import get_model_name, pagination
from deltago.models.cart import Cart
from deltago.models.commodity import BabyCare

def create_cart(item):
    new_cart = Cart(
        stockcode = item["stockcode"],
        model_name = item["model_name"],
        quantity = item["quantity"]
        )
    new_cart.save()

def create_carts(items):
    for item in items:
        create_cart(item)

def update(cart, increment):
    new_quantity = cart.quantity + increment
    cart.quantity = new_quantity
    cart.save()

def add_to_cart(stockcode, category, quantity):
    cart_list = Cart.objects.filter(stockcode=stockcode)

    if len(cart_list) > 0:
        cart = cart_list[0]
        update(cart, quantity)
    else:
        model_name = get_model_name(category)
        item = {
            "stockcode": stockcode,
            "model_name": model_name,
            "quantity": quantity
        }
        create_cart(item)
    

def get_product(cart):
    stockcode = cart.stockcode
    model_name = cart.model_name
    model = apps.get_model(app_label='deltago', model_name=model_name)
    return model.objects.get(stockcode=stockcode)

def get_cart_item(cart):
    product = get_product(cart)
    item = copy.copy(product)
    item.quantity = cart.quantity
    return item

def cart_list(page, per_page):
    carts = []
    list = Cart.objects.all()
    for item in list:
        cart_item = get_cart_item(item)
        carts.append(cart_item)
    result = pagination(carts, page, per_page)
    empty_tips = "购物车暂无商品"
    return {
        "products": result,
        "paginations": result,
        "empty_tips": empty_tips
    }