# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from deltago.models import Comment, Reviewship
from deltago.exceptions import errors

from deltago.views.services import share_service

def check_review_useful_available(comment, user):
    if comment.author == user:
        return (False, False)
    try:
        reviewship = Reviewship.objects.get(comment=comment, user=user)
        useful_available = bool(not reviewship.is_useful)
        unuseful_available = reviewship.is_useful
        return (useful_available, unuseful_available)
    except ObjectDoesNotExist:
        return (True, True)

def get_review_auth(comment, user):
    if user.is_superuser:
        return {'useful': True,'unuseful': True,'edit': True,'delete': True}
    if comment.author == user:
        return {'useful': False,'unuseful': False,'edit': True,'delete': True}
    else:
        review_auth = {'edit': False,'delete': False}
        review_auth['useful'], review_auth['unuseful'], = check_review_useful_available(comment, user)
        return review_auth

def get_review_number(comment):
    reviews = Reviewship.objects.filter(comment=comment)
    useful = reviews.filter(is_useful=True).count()
    unuseful = reviews.filter(is_useful=False).count()
    return useful, unuseful

def get_comment_list(comments, user):
    for comment in comments:
        (useful, unuseful) = get_review_number(comment)
        comment.useful_number = useful
        comment.unuseful_number = unuseful
        comment.review_auth = get_review_auth(comment, user)
    return comments

def get_comments(user, page, per_page):
    filter_comments = Comment.objects.filter(is_approved=True)
    comments = get_comment_list(filter_comments, user)
    paginations = share_service.pagination(comments, page, per_page)
    return {
        "comments": paginations,
        "paginations": paginations,
    }

def get_user_comments(user, page, per_page):
    filter_comments = Comment.objects.filter(author=user)
    user_comments = get_comment_list(filter_comments, user)
    paginations = share_service.pagination(filter_comments, page, per_page)
    return {
        "comments": paginations,
        "paginations": paginations,
    }

def create_comment(user, content, nickname, is_public):
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

def review(user, comment, is_useful):
    if user == comment.author:
        raise errors.OperationError('Operation Error')
    else:
        try:
            reviewship = Reviewship.objects.get(user=user, comment=comment)
            update_reviewship(reviewship, is_useful)
        except ObjectDoesNotExist:
            create_reviewship(user, comment, is_useful)

