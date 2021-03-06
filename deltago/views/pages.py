# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from deltago.views.services import page_service


def index(request):
    return render(request, 'deltago/index.html')

def search(request):
    content = request.GET.get('content')
    page = request.GET.get('page', 1)
    data = page_service.search_results(content, page, 20)
    return render(request, 'deltago/share/search_results.html', data)

def privacy(request):
    return render(request, 'deltago/pages/privacy.html')

def about(request):
    return render(request, 'deltago/pages/about.html')

def guides(request):
    return render(request, 'deltago/pages/guides.html')
