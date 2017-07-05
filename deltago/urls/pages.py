from django.conf.urls import url
from deltago.views import pages, babycare

urlpatterns = [
    url(r'^$', pages.index, name='index'),
    url(r'^babycare$', babycare.index, name='babycare'),
    url(r'^babycare/medicinal$', babycare.medicinal, name='medicinal'),
    url(r'^babycare/skincare$', babycare.skincare, name='skincare'),
    url(r'^babycare/nappy$', babycare.nappy, name='nappy'),
]