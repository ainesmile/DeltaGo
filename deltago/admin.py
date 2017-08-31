from django.contrib import admin
from deltago.models import commodity
from deltago.models import search
from deltago.models import cart
from deltago.models import order
from deltago.models import comment

admin.site.register(commodity.Commodity)
admin.site.register(commodity.Details)
admin.site.register(search.Search)
admin.site.register(cart.Cart)
admin.site.register(cart.Cartship)
admin.site.register(order.Order)
admin.site.register(order.Ship)
admin.site.register(order.Payment)
admin.site.register(comment.Comment)
admin.site.register(comment.Reply)
admin.site.register(comment.Reviewship)

