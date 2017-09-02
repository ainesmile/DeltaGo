# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from deltago.views.services import delivery_service

def create(request):
    user = request.user
    if request.method == 'POST':
        receiver = request.POST.get('receiver')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        new_delivery = delivery_service.create(user, receiver, contact_number, address)
        return redirect('cart')
    else:
        return render(request, 'deltago/deliver/create.html')


