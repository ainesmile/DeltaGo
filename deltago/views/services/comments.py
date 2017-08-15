# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from deltago.models import Comment, Reviewship
from deltago.exceptions import errors

from deltago.views.services import share

def get_comment_review_number(comment):
    reviews = Reviewship.objects.filter(comment=comment)
    useful = reviews.filter(is_useful=True).count()
    unuseful = reviews.filter(is_useful=False).count()
    return useful, unuseful

def get_comments(page, per_page):
    comments = Comment.objects.filter(is_approved=True)
    for comment in comments:
        (useful, unuseful) = get_comment_review_number(comment)
        comment.useful_number = useful
        comment.unuseful_number = unuseful
    paginations = share.pagination(comments, page, per_page)
    return {
        "comments": paginations,
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

def create_reviewship(user, comment, is_useful):
    new_reviewship = Reviewship(
        user=user,
        comment=comment,
        is_useful=is_useful)
    new_reviewship.save()

def update_reviewship(reviewship, is_useful):
    if bool(reviewship.is_useful) == bool(is_useful):
        raise errors.DuplicateError('duplicated review')
    else:
        reviewship.is_useful = bool(is_useful)
        reviewship.save()

def review_comment(user, comment, is_useful):
    try:
        reviewship = Reviewship.objects.get(user=user, comment=comment)
        update_reviewship(reviewship, is_useful)
    except ObjectDoesNotExist:
        create_reviewship(user, comment, is_useful)

def get_user_comments(user, page, per_page):
    filter_comments = Comment.objects.filter(author=user)
    paginations = share.pagination(filter_comments, page, per_page)
    return {
        "comments": paginations,
        "paginations": paginations,
    }
