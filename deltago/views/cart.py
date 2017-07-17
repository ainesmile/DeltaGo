from django.shortcuts import render, redirect
from deltago.models.cart import Cart

from services.cart import add_to_cart, cart_list



def cart(request):
    page = request.GET.get('page', 1)
    data = cart_list(page, 20)
    return render(request, 'deltago/cart/cart.html', data)


def addcart(request, category, stockcode):
    if request.method == 'POST':
        quantity = int(request.GET['quantity'])
        add_to_cart(stockcode, category, quantity)
    return redirect('cart')