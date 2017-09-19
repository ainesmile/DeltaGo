from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from deltago.models import Cart
from deltago.views.services import cart_service, order_service

@login_required(login_url='login')
def addcart(request, product_id):
    user = request.user
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cartship = cart_service.add_to_cart(user, product_id, quantity)
        if not cartship:
            return render(request, 'deltago/share/product_404.html')
        else:
            return redirect('cart')
    
@login_required(login_url='login')
def cart(request):
    user = request.user
    page = request.GET.get('page', 1)
    data = cart_service.get_cart_render_data(user, page, 20)
    data["check_fail"] = False
    if request.method == 'POST':
        quantities = request.POST.getlist('quantity')
        checkboxes = request.POST.getlist('checkbox')
        checkbox_all = bool(request.POST.get('checkbox_all'))
        delivery_id = request.POST.get('delivery_id')

        if delivery_id is None:
            return redirect('delivery_create')

        if checkboxes or checkbox_all:
            new_order = order_service.generate_order(user, checkboxes, quantities, checkbox_all, delivery_id)
            return redirect('order_pay', order_id=new_order.pk)
        else:
            data["check_fail"] = True
    return render(request, 'deltago/cart/cart.html', data)
        
