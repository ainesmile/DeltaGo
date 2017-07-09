from django.contrib import admin
from deltago.models import commodity
from deltago.models import search

admin.site.register(commodity.BabyCare)
admin.site.register(commodity.BabyCareDetails)
admin.site.register(search.Search)