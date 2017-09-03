from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseForbidden
from deltago.models import DeliverInfo

def create(user, delivery_info):
    kwargs = delivery_info
    kwargs["user"] = user
    new_delivery = DeliverInfo(**kwargs)
    new_delivery.save()
    return new_delivery

def get_delivery(user, delivery_id):
    try:
        delivery = DeliverInfo.objects.get(pk=delivery_id)
    except ObjectDoesNotExist:
        raise Http404()
    if delivery.user != user:
        raise HttpResponseForbidden()
    else:
        return delivery

def edit(user, delivery_id, delivery_info):
    delivery = get_delivery(user, delivery_id)
    delivery_info["user"] = user
    updated = DeliverInfo(pk=delivery.pk, **delivery_info)
    updated.save()

def delete(user, delivery_id):
    delivery = get_delivery(user, delivery_id)
    delivery.delete()