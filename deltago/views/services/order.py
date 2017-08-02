# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.models import User

from deltago.exceptions import errors

from deltago.models import Order, Cart, Cartship

from deltago.views.services.share import pagination
from deltago.views.services.cart import user_current_cart

SHIP_FEE = 500

def undelete_cartship(cartship):
    if cartship.is_deleted:
        cartship.is_deleted = False
        cartship.save()

def choose_cartship(cartship):
    cartship.is_chosen = True
    cartship.save()

def get_chosen_cartshipes(checkboxes):
    chosens = []
    for checkbox in checkboxes:
        cartship = Cartship.objects.get(pk=checkbox)
        undelete_cartship(cartship)
        choose_cartship(cartship)
        chosens.append(cartship)
    return chosens

def get_unchosen_cartshipes(all_cartshipes, chosens):
    return list(set(all_cartshipes) - set(chosens))

def update_quantities(all_cartshipes, quantities):
    for index, cartship in enumerate(all_cartshipes):
        quantity = quantities[index]
        cartship.quantity = quantity
        cartship.updated_date = timezone.now()
        cartship.save()

def archive_cart(cart):
    cart.is_archived = True
    cart.save()

def new_cart_with_unchosens(user, unchosens):
    new_cart = Cart(user=user)
    new_cart.save()
    for cartship in unchosens:
        cartship.cart = new_cart
        cartship.created_date = timezone.now()
        cartship.updated_date = timezone.now()
        cartship.save()

def get_price(commodity):
    price = commodity.price or commodity.was_price
    return float(price) * 100

def get_commodity_total(cartship):
    commodity = cartship.commodity
    price = get_price(commodity)
    quantity = cartship.quantity
    return price * quantity

def get_subtotal(cartshipes):
    subtotal = 0
    for cartship in cartshipes:
        subtotal += get_commodity_total(cartship)
    return subtotal

def init_order(cart, subtotal, total):
    user = cart.user
    new_order = Order(
        user=user,
        cart=cart,
        subtotal=subtotal,
        total=total)
    new_order.save()
    return new_order

def create_order_by_chosen(current_cart, chosens):
    subtotal = get_subtotal(chosens)
    total = subtotal + SHIP_FEE
    new_order = init_order(current_cart, subtotal, total)
    return new_order
    
def generate_order(user, checkboxes, quantities):
    current_cart = user_current_cart(user)
    # 1. update_all_cartship_quantity
    all_cartshipes = Cartship.objects.filter(cart=current_cart)
    update_quantities(all_cartshipes, quantities)
    # 2. update_cartship_is_chosen 3. undeleted
    chosens = get_chosen_cartshipes(checkboxes)
    if not chosens:
        raise errors.EmptyCartError("Choose at least one item.")
    else:
        # 4. mark cart archived
        archive_cart(current_cart)
        # 5. create new cart with unchosen cartshipes
        unchosens = get_unchosen_cartshipes(all_cartshipes, chosens)
        new_cart_with_unchosens(user, unchosens)
        # 6. create order
        new_order = create_order_by_chosen(current_cart, chosens)
        return new_order
        





# Order display

def order_list(user, page, per_page):
    data = Order.objects.filter(user=user)
    orders = pagination(data, page, per_page)
    empty_tips = '还没有订单哦~'
    return {
        "orders": orders,
        "paginations": orders,
        "empty_tips": empty_tips
    }


def convert_fee(amount):
    return amount / float(100)

def get_order_fee(order):
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

def get_commodity_table_item(cartship):
    price = get_price(cartship.commodity)
    show_price = convert_fee(price)
    commodity_total = convert_fee(price * cartship.quantity)
    return {
        "commodity": cartship.commodity,
        "price": show_price,
        "quantity": cartship.quantity,
        "commodity_total": commodity_total
    }

def get_commodity_info_table(order):
    table = []
    cart = order.cart
    cartshipes = Cartship.objects.filter(cart=cart)
    for cartship in cartshipes:
        item = get_commodity_table_item(cartship)
        table.append(item)
    return table

def get_order_state_text(state):
    state_text = {
        'U': '未支付',
        'P': '正在处理',
        'F': '已完成',
        'C': '正在取消',
        'A': '已取消',
    }
    return state_text[state]

def get_order_details(order_id):
    order = Order.objects.get(pk=order_id)
    order.fee = get_order_fee(order)
    order.commodity_info_table = get_commodity_info_table(order)
    order.state_text = get_order_state_text(order.state)
    return order

