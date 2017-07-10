from django.conf.urls import url
from deltago.views import pages, babycare

urlpatterns = [
    url(r'^$', pages.index, name='index'),
    url(r'^search/$', pages.search, name='search'),
    url(r'^babycare/babyfood-from-(?P<month>\w+)-mths/$', babycare.food, name='food'),
    url(r'^babycare/medicinal$', babycare.medicinal, name='medicinal'),
    url(r'^babycare/skincare$', babycare.skincare, name='skincare'),
    url(r'^babycare/nappy$', babycare.nappy, name='nappy'),
    url(r'^babycare/(?P<stockcode>\w+)/$', babycare.details, name='details'),
]