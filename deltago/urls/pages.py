from django.conf.urls import url
from deltago.views import pages

urlpatterns = [
    url(r'^$', pages.index, name='index'),
    url(r'^search/$', pages.search, name='search'),
    url(r'^privacy/$', pages.privacy, name='privacy'),
    url(r'^about/$', pages.about, name='about'),
]