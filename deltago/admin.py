from django.contrib import admin
from deltago.models import commodity, nutrition

admin.site.register(commodity.BabyCare)
admin.site.register(commodity.BabyCareDetails)
admin.site.register(nutrition.Nutrition)