from django.conf.urls import url
from deltago.views import order

urlpatterns = [
    url(r'^checkout$', order.checkout, name='checkout'),
    url(r'^order$', order.order, name='order'),
]