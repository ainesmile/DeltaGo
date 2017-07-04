from django.shortcuts import render
from services.share import pagination
from deltago.models import BabyCare

def index(request):
    products = BabyCare.objects.filter(sub_category="F")
    page = request.GET.get('page', 1)
    paginations = pagination(products, page, 20)
    return render(request, 'deltago/babycare/index.html', {
        "products": paginations,
        "paginations": paginations,
        })

def medicinal(request):
    products = BabyCare.objects.filter(sub_category="M")
    page = request.GET.get('page', 1)
    paginations = pagination(products, page, 20)
    return render(request, 'deltago/babycare/index.html', {
        "products": paginations,
        "paginations": paginations,
        })