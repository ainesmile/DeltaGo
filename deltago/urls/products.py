from django.conf.urls import url
from deltago.views import products

urlpatterns = [
    url(r'(?P<categ_name>\w+)/(?P<sub_name>\w+)$', products.products, name='products'),
]