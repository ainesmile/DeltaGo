from django.shortcuts import render, redirect
from deltago.models import Cart, Order

def checkout(request):
    # if request.method == 'POST':
    #     quantities = request.POST.getlist('quantity')
    #     checkboxes = request.POST.getlist('checkbox')
    return redirect('index')