from django.apps import apps
from deltago.models import Order, Cart

# def create(item):
#     fields = [
#         "commodities", "prices", "quantities", "state", "payment_method",
#         "ship_address", "exchange_rate", "subtotal", "total", "user",
#         "unpaind_time", "archived_time", "processing_time", "canceling_time", "finished_time"
#     ]
#     for f in fields:
#         kwargs[f] = item[f]
#     new_order = Order.objects.create(**kwargs)

# def get_commodity(cart_id):
#     cart = Cart.objects.get(pk=cart_id)
#     model_name = cart.model_name
#     commodity_id = cart.commodity_id
#     model = apps.get_model('deltago', model_name=model_name)
#     return model.objects.get(pk=commodity_id)


# def get_commodities(checkboxes):
#     commodities = []
#     for checkbox in checkboxes:
#         commodity = get_commodity(checkbox)
#         commodities.append(commodity)
#     return commodities