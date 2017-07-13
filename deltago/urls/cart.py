from django.conf.urls import url
from deltago.views import cart

urlpatterns = [
    url(r'^cart/$', cart.cart, name="cart"),
    url(r'^addcart/(?P<category>\w+)/(?P<stockcode>\w+)/$', cart.addcart, name="addcart")
]