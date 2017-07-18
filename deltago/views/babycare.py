from django.shortcuts import render
from services.babycare import render_data, details_render_data, month_category
from deltago.models import BabyCare, BabyCareDetails

def food(request, month):
    sub_category = month_category(month)
    condition = {"sub_category": sub_category}
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

def details(request, commodity_id):
    data = details_render_data(commodity_id)
    return render(request, 'deltago/babycare/details.html', data)
