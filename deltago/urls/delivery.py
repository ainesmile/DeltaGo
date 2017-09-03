from django.conf.urls import url
from deltago.views import delivery

urlpatterns = [
    url(r'^delivery/create$', delivery.create, name='delivery_create'),
    url(r'^delivery/(?P<delivery_id>\w+)/edit$', delivery.edit, name='delivery_edit'),
    url(r'^delivery/(?P<delivery_id>\w+)/delete', delivery.delete, name="delivery_delete"),
]