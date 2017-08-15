from django.conf.urls import url
from deltago.views import comments

urlpatterns = [
    url(r'^comments/$', comments.comments, name='comments'),
    url(r'^comments/add$', comments.add_comment, name='add_comment'),
    url(r'^comments/review/(?P<comment_id>\w+)/(?P<is_useful>\d)$', comments.review, name="review"),
    url(r'^comments/delete/(?P<comment_id>\w+)$', comments.delete_comment, name="delete_comment"),
]