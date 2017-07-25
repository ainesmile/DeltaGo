from django.shortcuts import render, redirect

from services.cart import add_to_cart


def cart(request):
    return redirect('index')


def addcart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        new_cart = add_to_cart(product_id, quantity)
        if not new_cart:
            return render(request, 'deltago/share/product_404.html')
        else:
            return redirect('index')
    