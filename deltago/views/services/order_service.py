# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from django.utils import timezone
import random

from django.contrib.auth.models import User

from deltago.exceptions import errors

from deltago.models import Order, Cart, Cartship, Ship, DeliverInfo

from deltago.views.services import cart_service, share_service

from deltago.templatetags import date


# A. help functions

# A1 generate order help functions

def get_order(order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except ObjectDoesNotExist:
        raise Http404('该订单不存在')
    return order

def check_order_cancellable(user, order):
    if (not user.is_authenticated) or (user != order.user):
        raise PermissionDenied
    else:
        return bool(order.state == Order.UNPAID)

def check_user_permission(user, order):
    if user != order.user:
        raise PermissionDenied


def create_ship_based_delivery(order, delivery_info_id):
    try:
        info_id = int(delivery_info_id)
        info = DeliverInfo.objects.get(pk=info_id)
    except ValueError:
        return None
    except ObjectDoesNotExist:
        raise Http404()
    new_ship = Ship(
        order=order,
        receiver=info.receiver,
        contact_number=info.contact_number,
        address=info.address)
    new_ship.save()
    return new_ship



# 1. update_quantities_checked_deleted_states_based_on_current_cart
def update_cartships(current_cart, checkboxes, quantities, checkbox_all):
    cartships = Cartship.objects.filter(cart=current_cart)
    for index, cartship in enumerate(cartships):
        is_chosen = checkbox_all or (unicode(cartship.pk) in checkboxes)
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


# TODO
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
def init_order(cart, subtotal, ship_fee):
    user = cart.user
    new_order = Order(
        user=user,
        cart=cart,
        subtotal=subtotal)

    new_order.total = subtotal + ship_fee + new_order.service_charge
    new_order.serial_code = generate_order_serial_code(new_order)
    new_order.save()
    return new_order

def new_order_with_chosen(current_cart, chosens):
    subtotal = share_service.get_cartships_subtotal(chosens)
    ship_fee = share_service.cal_ship_fee(chosens)
    total = subtotal + ship_fee
    new_order = init_order(current_cart, subtotal, ship_fee)
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

def get_order_show_fee(order):
    subtotal = order.subtotal
    total = order.total
    service = order.service_charge
    ship_fee = total - subtotal - service
    exchange_rate = order.exchange_rate
    rmb = round(float(total * exchange_rate) / 100, 2)
    return {
        "subtotal": subtotal,
        "service": service, 
        "total": total,
        "ship_fee": ship_fee,
        "exchange_rate": exchange_rate,
        "rmb": rmb
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

def get_order_ship_details(user, order):
    try:
        ship = Ship.objects.get(order=order)
    except:
        raise Http404()
    check_user_permission(user, order)
    return {
        "receiver": ship.receiver,
        "address": ship.address,
        "contact_number": ship.contact_number,
        "express_name": ship.express_name,
        "express_number": ship.express_number,
        "state": ship.state
    }

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
    price = cartship.commodity.price
    commodity_total = share_service.get_cartship_subtotal(cartship)
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
def generate_order(user, checkboxes, quantities, checkbox_all, delivery_info_id):
    current_cart = cart_service.user_current_cart(user)
    update_cartships(current_cart, checkboxes, quantities, checkbox_all)
    chosens = Cartship.objects.filter(cart=current_cart, is_chosen=True)
    if not chosens:
        # raise errors.EmptyCartError("Choose at least one item.")
        raise Http404()
    else:
        archive_cart(current_cart)
        new_order = new_order_with_chosen(current_cart, chosens)
        create_ship_based_delivery(new_order, delivery_info_id)
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
def get_order_details(user, order_id):
    order = get_order(order_id)
    check_user_permission(user, order)
    order = get_order_basic_info(order)
    order.commodity_info_table = get_commodity_info_table(order)
    order.ship_details = get_order_ship_details(user, order)
    return order

# B4 pay order view
def get_pay_data(user, order_id):
    order = get_order(order_id)
    check_user_permission(user, order)
    order.rmb = round(float(order.total * order.exchange_rate)/100, 2)
    order.ship_details = get_order_ship_details(user, order)
    return order


def cancel_order(user, order_id):
    order = get_order(order_id)
    is_cancellable = check_order_cancellable(user, order)
    if is_cancellable:
        order.state = Order.ARCHIVED
        order.save()
    return is_cancellable



