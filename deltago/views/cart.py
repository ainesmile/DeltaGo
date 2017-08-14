from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from deltago.models import Cart
from services.cart import add_to_cart, cartship_list

@login_required(login_url='login')
def cart(request):
    user = request.user
    page = request.GET.get('page', 1)
    data = cartship_list(user, page, 20)
    return render(request, 'deltago/cart/cart.html', data)

@login_required(login_url='login')
def addcart(request, product_id):
    user = request.user
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cartship = add_to_cart(user, product_id, quantity)
        if not cartship:
            return render(request, 'deltago/share/product_404.html')
        else:
            return redirect('cart')
    
