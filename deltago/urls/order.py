from django.conf.urls import url
from deltago.views import order

urlpatterns = [
    url(r'^orders/mine$', order.my_orders, name='my_orders'),
    url(r'^orders/details/(?P<order_id>\w+)$', order.order_details, name='order_details'),
    url(r'^order/(?P<order_id>\w+)/pay$', order.order_pay, name='order_pay'),
    url(r'^order/(?P<order_id>\w+)/cancel$', order.order_cancel, name='order_cancel'),
    url(r'^order/(?P<order_id>\w+)/reorder$', order.order_reorder, name='order_reorder'),
]