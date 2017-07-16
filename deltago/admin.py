from django.contrib import admin
from deltago.models import commodity
from deltago.models import search
from deltago.models import cart
from deltago.models import order

admin.site.register(commodity.BabyCare)
admin.site.register(commodity.BabyCareDetails)
admin.site.register(search.Search)
admin.site.register(cart.Cart)
admin.site.register(order.Order)
admin.site.register(order.Ship)
admin.site.register(order.Payment)