from django.conf.urls import url
from deltago.views import delivery

urlpatterns = [
    url(r'^delivery/create$', delivery.create, name='delivery_create'),
]