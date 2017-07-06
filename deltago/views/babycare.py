from django.shortcuts import render
from services.babycare import render_data, details_render_data
from deltago.models import BabyCare, BabyCareDetails

def index(request):
    condition = {"sub_category": "F4"}
    page = request.GET.get('page', 1)
    data = render_data(condition, page, 20)
    return render(request, 'deltago/babycare/base.html', data)

def medicinal(request):
    condition = {"sub_category": "M"}
    page = request.GET.get('page', 1)
    data = render_data(condition, page, 20)
    return render(request, 'deltago/babycare/base.html', data)

def skincare(request):
    condition = {"sub_category": "T"}
    page = request.GET.get('page', 1)
    data = render_data(condition, page, 20)
    return render(request, 'deltago/babycare/base.html', data)

def nappy(request):
    condition = {"sub_category": "N"}
    page = request.GET.get('page', 1)
    data = render_data(condition, page, 20)
    return render(request, 'deltago/babycare/base.html', data)

def details(request, stockcode):
    data = details_render_data(stockcode)
    return render(request, 'deltago/babycare/details.html', data)
