from django.conf.urls import url
from django.contrib.auth import views as auth_views
from deltago.views import account

urlpatterns = [
    url(r'^login/$', account.login_view, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^password/reset$', account.password_reset_view, name='password_reset'),
    url(r'^password/reset/(?P<user_id>\w+)/$', account.password_reset_repeat_view, name='password_reset_repeat'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        account.password_reset_token_view, name='password_reset_token'),
    url(r'^password/change$', account.password_change_view, name='password_change'),
    url(r'^password/change/done$', auth_views.password_change_done, {
        'template_name': 'deltago/registration/password_change_done.html'}, name='password_change_done'),
    url(r'^register/$', account.register, name="register"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        account.activate_view, name='activate'),
    url(r'^activate/(?P<user_id>\w+)/$', account.activate_email_view, name="activate_email"),
    url(r'^activate/repeat/(?P<user_id>\w+)/$', account.activate_email_repeat_view, name="activate_email_repeat"),
    url(r'^activate/email/send$', account.activate_email_form_view, name="activate_email_form"),
    
]
