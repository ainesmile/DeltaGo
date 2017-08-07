from django.conf.urls import url
from deltago.views import comments

urlpatterns = [
    url(r'^comments/$', comments.comments, name='comments'),
    url(r'^comments/add$', comments.add_comment, name='add_comment'),
]