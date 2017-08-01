from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from deltago.exceptions import errors
from deltago.views.services.order import order_list


def checkout(request):
    # user = request.user
    user = User.objects.get(pk=1)
    if request.method == 'POST':
        quantities = request.POST.getlist('quantity')
        checkboxes = request.POST.getlist('checkbox')
        try:
            order.generate_order(user, checkboxes, quantities)
        except errors.EmptyCartError:
            print 'please choose at least one item'
    return redirect('order')

def order(request):
    # user = request.user
    user = User.objects.get(pk=1)
    page = request.GET.get('page', 1)
    data = order_list(user, page, 20)
    return render(request, 'deltago/order/order.html', data)