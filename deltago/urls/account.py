from django.conf.urls import url
from django.contrib.auth import views as auth_views
from deltago.views import account

urlpatterns = [
    url(r'^login/$', account.login_view, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^password/reset$', account.password_reset_view, name='password_reset'),
    url(r'^password/reset/done$', account.password_reset_done_view, name='password_reset_done'),
]