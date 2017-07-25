from django.shortcuts import render, redirect

from services.cart import add_to_cart, cart_list

def cart(request):
    page = request.GET.get('page', 1)
    data = cart_list(page, 20)
    return render(request, 'deltago/cart/cart.html', data)

def addcart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        new_cart = add_to_cart(product_id, quantity)
        if not new_cart:
            return render(request, 'deltago/share/product_404.html')
        else:
            return redirect('cart')
    