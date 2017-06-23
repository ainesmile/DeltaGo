from django.conf.urls import url
from deltago.views import pages

urlpatterns = [
    url(r'^$', pages.index, name='index'),
    url(r'^babycare$', pages.babycare, name='babycare'),
]