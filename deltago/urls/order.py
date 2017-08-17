from django.conf.urls import url
from deltago.views import order

urlpatterns = [
    url(r'^checkout$', order.checkout, name='checkout'),
    url(r'^orders/mine$', order.my_orders, name='my_orders'),
    url(r'^orders/details/(?P<order_id>\w+)$', order.order_details, name='order_details'),
]