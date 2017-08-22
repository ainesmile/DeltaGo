from django.conf.urls import url
from deltago.views import products

urlpatterns = [
    url(r'^products$', products.products, name='products'),
]