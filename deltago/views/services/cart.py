from django.shortcuts import get_object_or_404
from .share import get_model
from deltago.models import Cart

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
        model_name = get_model(category)
        item = {
            "stockcode": stockcode,
            "model_name": model_name,
            "quantity": quantity
        }
        create_cart(item)
    
    
    