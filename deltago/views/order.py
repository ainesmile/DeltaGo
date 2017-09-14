from django.shortcuts import render, redirect
from django.http import Http404
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
        checkbox_all = bool(request.POST.get('checkbox_all'))
        delivery_id = request.POST.get('delivery_id')
        new_order = order_service.generate_order(user, checkboxes, quantities, checkbox_all, delivery_id)
    return redirect('order_pay', order_id=new_order.pk)


@login_required(login_url='login')
def my_orders(request):
    user = request.user
    page = request.GET.get('page', 1)
    data = order_service.get_order_list(user, page, 20)
    return render(request, 'deltago/order/order.html', data)

@login_required(login_url='login')
def order_details(request, order_id):
    user = request.user
    details = order_service.get_order_details(order_id)
    return render(request, 'deltago/order/details.html', {"order": details})

def order_pay(request, order_id):
    pay_data = order_service.get_pay_data(order_id)
    return render(request, 'deltago/order/pay.html', {"order": pay_data})


