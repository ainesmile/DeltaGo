from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from deltago.exceptions import errors
from deltago.views.services.order import generate_order, order_list, get_order_details

@login_required(login_url='login')
def checkout(request):
    user = request.user
    if request.method == 'POST':
        quantities = request.POST.getlist('quantity')
        checkboxes = request.POST.getlist('checkbox')
        try:
            generate_order(user, checkboxes, quantities)
        except errors.EmptyCartError:
            print 'please choose at least one item'
    return redirect('order')

@login_required(login_url='login')
def order(request):
    user = request.user
    page = request.GET.get('page', 1)
    data = order_list(user, page, 20)
    return render(request, 'deltago/order/order.html', data)

@login_required(login_url='login')
def order_details(request, order_id):
    user = request.user
    order_details = get_order_details(order_id)
    return render(request, 'deltago/order/details.html', {"order": order_details})