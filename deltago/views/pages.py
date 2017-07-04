from django.shortcuts import render
from services.share import pagination

def index(request):
    return render(request, 'deltago/index.html')

