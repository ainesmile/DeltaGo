from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from deltago.exceptions import errors
from deltago.views.services import order_service

@login_required(login_url='login')
def checkout(request):
    user = request.user
    if request.method == 'POST':
        quantities = request.POST.getlist('quantity')
        checkboxes = request.POST.getlist('checkbox')
        checkbox_all = request.POST.getlist('checkbox_all')
        try:
            order_service.generate_order(user, checkboxes, quantities, checkbox_all)
        except errors.EmptyCartError:
            print 'please choose at least one item'
    return redirect('order')

@login_required(login_url='login')
def my_orders(request):
    user = request.user
    page = request.GET.get('page', 1)
    data = order_service.get_order_list(user, page, 20)
    return render(request, 'deltago/order/order.html', data)

@login_required(login_url='login')
def order_details(request, order_id):
    user = request.user
    order_details = order_service.get_order_details(order_id)
    return render(request, 'deltago/order/details.html', {"order": order_details})