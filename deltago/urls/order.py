from django.conf.urls import url
from deltago.views import order

urlpatterns = [
    url(r'^order/checkout$', order.checkout, name='checkout'),
]