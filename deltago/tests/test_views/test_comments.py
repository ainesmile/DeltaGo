from django.test import TestCase
from django.utils import timezone
from django.core.paginator import Page
from django.contrib.auth.models import User

from deltago.models import Comment

from deltago.views.services import comments

class CommentViewTest(TestCase):

    fixtures = [
        'deltago/fixtures/user.json',
        'deltago/fixtures/comments.json',
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.comment_1 = Comment.objects.get(pk=1)

        self.content = 'content'
        self.nickname = 'nickname'

    def test_creat_comment(self):
        new_comment = comments.creat_comment(self.user, self.content, self.nickname, True)
        self.assertEqual(new_comment.content, self.content)
        self.assertEqual(new_comment.nickname, self.nickname)
        self.assertEqual(new_comment.author, self.user)
