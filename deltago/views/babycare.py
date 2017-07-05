from django.shortcuts import render
from services.babycare import render_data
from deltago.models import BabyCare

def index(request):
    condition = {"sub_category": "F"}
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