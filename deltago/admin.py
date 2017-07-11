from django.contrib import admin
from deltago.models import commodity
from deltago.models import search
from deltago.models import cart

admin.site.register(commodity.BabyCare)
admin.site.register(commodity.BabyCareDetails)
admin.site.register(search.Search)
admin.site.register(cart.Cart)