from django.conf.urls import url
from deltago.views import cart

urlpatterns = [
    url(r'^carts/$', cart.cart, name="cart"),
    url(r'^cart/add/(?P<product_id>\w+)$', cart.addcart, name="addcart"),
]