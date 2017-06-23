from django.shortcuts import render
from services.share import pagination

from deltago.models import BabyCare

def index(request):
    return render(request, 'deltago/index.html')

def babycare(request):
    babycares = BabyCare.objects.all()
    page = request.GET.get('page', 1)
    paginations = pagination(babycares, page, 20)
    return render(request, 'deltago/babycare.html', {
        "babycares": paginations,
        "paginations": paginations,
        })