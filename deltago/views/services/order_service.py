# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.utils import timezone
import random

from django.contrib.auth.models import User

from deltago.exceptions import errors

from deltago.models import Order, Cart, Cartship

from deltago.views.services import cart_service, share_service

from deltago.templatetags import date


SHIP_FEE = 500

# A. help functions

# A1 generate order help functions

# 1. update_quantities_checked_deleted_states_based_on_current_cart
def update_cartships(current_cart, checkboxes, quantities, checkbox_all):
    cartships = Cartship.objects.filter(cart=current_cart)
    for index, cartship in enumerate(cartships):
        is_chosen = checkbox_all or (cartship.pk in checkboxes)
        cartship.is_chosen = is_chosen
        if is_chosen and cartship.is_deleted:
            cartship.is_deleted = False
        cartship.quantity = quantities[index]
        cartship.updated_date = timezone.now()
        cartship.save()
    return cartships

def archive_cart(cart):
    cart.is_archived = True
    cart.save()

def generate_order_serial_code(order):
    serial_code = ''
    unpaid_time = order.unpaid_time
    dates = [
        unpaid_time.year, unpaid_time.month, unpaid_time.day,
        unpaid_time.second, unpaid_time.microsecond]
    for item in dates:
        serial_code += date.padding_date(item)
    random_str = str(random.sample(xrange(9999), 1)[0])
    length = 4 - len(random_str)
    serial_code += random_str + '0' * length
    return serial_code

# create new order with chosen cartships
def init_order(cart, subtotal, total):
    user = cart.user
    new_order = Order(
        user=user,
        cart=cart,
        subtotal=subtotal,
        total=total)
    new_order.serial_code = generate_order_serial_code(new_order)
    new_order.save()
    return new_order

def new_order_with_chosen(current_cart, chosens):
    subtotal = share_service.get_cartships_subtotal(chosens)
    total = subtotal + SHIP_FEE
    new_order = init_order(current_cart, subtotal, total)
    return new_order

# create new cart with unchosen cartships
def new_cart_with_unchosens(user, unchosens):
    new_cart = Cart(user=user)
    new_cart.save()
    for cartship in unchosens:
        cartship.cart = new_cart
        cartship.created_date = timezone.now()
        cartship.updated_date = timezone.now()
        cartship.save()
    return new_cart

# A2 display order list help functions
def convert_fee(amount):
    return amount / float(100)

def get_order_show_fee(order):
    subtotal = convert_fee(order.subtotal)
    total = convert_fee(order.total)
    ship_fee = total - subtotal
    exchange_rate = convert_fee(order.exchange_rate)
    return {
        "subtotal": subtotal,
        "total": total,
        "ship_fee": ship_fee,
        "exchange_rate": exchange_rate
    }

def get_order_state_text(state):
    state_text = {
        'U': '未支付',
        'P': '正在处理',
        'F': '已完成',
        'C': '正在取消',
        'A': '已取消',
    }
    return state_text[state]

def get_order_basic_info(order):
    order.fee = get_order_show_fee(order)
    order.state_text = get_order_state_text(order.state)
    return order

def get_order_list_basic_info(orders):
    for order in orders:
        get_order_basic_info(order)
    return orders


# A3 display order details help functions
def get_commodity_info_table_item(cartship):
    price = convert_fee(cartship.commodity.price)
    commodity_total = convert_fee(share_service.get_cartship_subtotal(cartship))
    return {
        "commodity": cartship.commodity,
        "price": price,
        "quantity": cartship.quantity,
        "commodity_total": commodity_total
    }

def get_commodity_info_table(order):
    table = []
    cart = order.cart
    cartships = Cartship.objects.filter(cart=cart)
    for cartship in cartships:
        item = get_commodity_info_table_item(cartship)
        table.append(item)
    return table

# B exported view functions

# B1 checkout view
def generate_order(user, checkboxes, quantities, checkbox_all):
    current_cart = cart_service.user_current_cart(user)
    update_cartships(current_cart, checkboxes, quantities, checkbox_all)
    chosens = Cartship.objects.filter(cart=current_cart, is_chosen=True)
    if not chosens:
        raise errors.EmptyCartError("Choose at least one item.")
    else:
        archive_cart(current_cart)
        new_order = new_order_with_chosen(current_cart, chosens)
        unchosens = Cartship.objects.filter(cart=current_cart, is_chosen=False)
        if unchosens:
            new_cart_with_unchosens(user, unchosens)
        return new_order

# B2 my_orders view
def get_order_list(user, page, per_page):
    order_filter = Order.objects.filter(user=user)
    data = get_order_list_basic_info(order_filter)
    orders = share_service.pagination(data, page, per_page)
    empty_tips = '还没有订单哦~'
    return {
        "orders": orders,
        "paginations": orders,
        "empty_tips": empty_tips
    }

# B3 order_details view
def get_order_details(order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except ObjectDoesNotExist:
        raise Http404('该订单不存在')

    order = get_order_basic_info(order)
    order.commodity_info_table = get_commodity_info_table(order)
    return order
