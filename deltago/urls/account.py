from django.conf.urls import url
from django.contrib.auth import views as auth_views
from deltago.views import account

urlpatterns = [
    url(r'^login/$', account.login_view, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]