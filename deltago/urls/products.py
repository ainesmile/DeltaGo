from django.conf.urls import url
from deltago.views import products

urlpatterns = [
    url(r'^products$', products.product_view, name='products'),
    url(r'^products/(?P<commodity_id>\w+)$', products.details_view, name='product_details'),
]