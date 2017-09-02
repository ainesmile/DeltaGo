from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('deltago.urls.pages')),
    url(r'', include('deltago.urls.products')),
    url(r'', include('deltago.urls.cart')),
    url(r'', include('deltago.urls.order')),
    url(r'', include('deltago.urls.comments')),
    url(r'', include('deltago.urls.account')),
    url(r'', include('deltago.urls.delivery')),
]
