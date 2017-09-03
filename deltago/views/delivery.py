# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from deltago.views.services import delivery_service

def get_delivery_from_post(post):
    receiver = post.get('receiver')
    contact_number = post.get('contact_number')
    address = post.get('address')
    return {
        "receiver": receiver,
        "contact_number": contact_number,
        "address": address
    }

@login_required(login_url='login')
def create(request):
    user = request.user
    if request.method == 'POST':
        delivery_info = get_delivery_from_post(request.POST)
        new_delivery = delivery_service.create(user, delivery_info)
        return redirect('cart')
    else:
        return render(request, 'deltago/deliver/create.html')

@login_required(login_url='login')
def edit(request, delivery_id):
    user = request.user
    delivery = delivery_service.get_delivery(user, delivery_id)
    if request.method == 'POST':
        delivery_info = get_delivery_from_post(request.POST)
        delivery_service.edit(user, delivery_id, delivery_info)
        return redirect('cart')
    else:
        return render(request, 'deltago/deliver/edit.html', {
            "delivery": delivery})

@login_required(login_url='login')
def delete(request, delivery_id):
    user = request.user
    delivery_service.delete(user, delivery_id)
    return redirect('cart')
