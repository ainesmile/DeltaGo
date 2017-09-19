from django.test import TestCase, Client
from django.utils import timezone
from django.core.paginator import Page
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.models import User

from deltago.exceptions import errors

from deltago.models import Comment, Reviewship

from deltago.views.services import comment_service

class CommentViewTest(TestCase):

    fixtures = [
        'deltago/fixtures/user.json',
        'deltago/fixtures/comments.json',
        'deltago/fixtures/reviewship.json',
    ]

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.user_1 = User.objects.get(pk=2)
        self.comment_1 = Comment.objects.get(pk=1)
        self.reviewship_1 = Reviewship.objects.get(pk=1)
        self.reviewship_2 = Reviewship.objects.get(pk=2)

        c = Client()
        response = c.get('comments')
        request = response.wsgi_request
        self.page = request.GET.get('page', 1)

        self.content = 'content'
        self.nickname = 'nickname'

    def test_get_review_number(self):
        result = comment_service.get_review_number(self.comment_1)
        self.assertEqual((1, 1), result)
