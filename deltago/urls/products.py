from django.conf.urls import url
from deltago.views import products

urlpatterns = [
    url(r'(?P<categ_name>\w+)/(?P<sub_categ_name>[0-9a-zA-Z\-]+)$', products.sub_category, name='sub_category'),
]