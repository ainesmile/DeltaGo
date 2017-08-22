from django.shortcuts import render, redirect
from deltago.models import Commodity
from deltago.views.services import product_service

def product_view(request):
    page = request.GET.get('page', 1)
    render_data = product_service.products(page, 20)
    return render(request, 'deltago/commodity/products.html', render_data)
