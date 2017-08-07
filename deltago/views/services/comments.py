# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from deltago.models import Comment

from deltago.views.services import share

def get_comments(page, per_page):
    comments = Comment.objects.filter(is_approved=True)
    sorted_comments = sorted(comments, key=lambda item: (item.useful_number - item.unuseful_number), reverse=True)
    paginations = share.pagination(sorted_comments, page, per_page)
    return {
        "comments": sorted_comments,
        "paginations": paginations,
    }

def creat_comment(user, content, nickname, is_public):
    new_comment = Comment(
        author=user,
        content=content,
        nickname=nickname,
        is_public=is_public)
    new_comment.save()
    return new_comment