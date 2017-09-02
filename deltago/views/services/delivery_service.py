from deltago.models import DeliverInfo

def create(user, receiver, contact_number, address):
    new_delivery = DeliverInfo(
        user=user,
        receiver=receiver,
        contact_number=contact_number,
        address=address
        )
    new_delivery.save()
    return new_delivery