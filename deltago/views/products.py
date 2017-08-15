from django.shortcuts import render, redirect

from deltago.views.services import product_service

def products(request):
    pass

def sub_category(request, categ_name, sub_categ_name):
    page = request.GET.get("page", 1)
    data = product_service.sub(categ_name, sub_categ_name, page, 20)
    return render(request, 'deltago/commodity/products.html', data)

def details(request, product_id):
    data = product_service.get_details(product_id)
    return render(request, 'deltago/commodity/details.html', data)
    