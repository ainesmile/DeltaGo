# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from deltago.models import Comment, Reviewship, Reply
from deltago.exceptions import errors

from deltago.views.services import share_service

def create_comment(user, content, nickname, is_public):
    new_comment = Comment(
        author=user,
        content=content,
        nickname=nickname,
        is_public=is_public)
    new_comment.save()
    return new_comment

def review(user, comment_id, is_useful):
    comment = get_comment(comment_id)
    if user == comment.author:
        raise PermissionDenied
    reviewship = check_reviewship_exist(comment, user)
    if reviewship is None:
        create_reviewship(user, comment, is_useful)
    else:
        if bool(is_useful) == bool(reviewship.is_useful):
            raise PermissionDenied
        else:
            reviewship.is_useful = is_useful
            reviewship.save()

def reply(user, comment, content, keep_private):
    if not user.is_superuser:
        raise PermissionDenied
    if keep_private is not None:
        is_public = False
    else:
        is_public = comment.is_public
    new_reply = Reply(
        comment=comment,
        author=user,
        content=content,
        is_public=is_public
        )
    new_reply.save()
    return new_reply

def delete(user, comment_id):
    comment = get_comment(comment_id)
    if check_delete_auth(comment, user):
        return comment
    else:
        raise PermissionDenied
            

# get all approved and public comments
def get_comments(user, page, per_page):
    filter_condition = {}
    if not user.is_superuser:
        filter_condition["is_approved"] = True
        filter_condition["is_public"] = True

    filter_comments = Comment.objects.filter(**filter_condition)
    comments = get_comments_details(filter_comments, user)
    paginations = share_service.pagination(comments, page, per_page)
    return {
        "comments": paginations,
        "paginations": paginations,
    }

def get_user_comments(user, page, per_page):
    filter_comments = Comment.objects.filter(author=user)
    user_comments = get_comments_details(filter_comments, user)
    paginations = share_service.pagination(user_comments, page, per_page)
    return {
        "comments": paginations,
        "paginations": paginations,
    }


def get_comments_details(comments, user):
    for comment in comments:
        (useful, unuseful) = get_review_number(comment)
        comment.useful_number = useful
        comment.unuseful_number = unuseful
        comment.auth = check_comment_auth(comment, user)
        comment.replies = get_replies(user, comment)
    return comments

def get_review_number(comment):
    reviews = Reviewship.objects.filter(comment=comment)
    useful = reviews.filter(is_useful=True).count()
    unuseful = reviews.filter(is_useful=False).count()
    return useful, unuseful

def get_replies(user, comment):
    filter_condition = {
        "comment": comment
    }
    if not (user.is_superuser or (user == comment.author)):
        filter_condition["is_public"] = True
    return Reply.objects.filter(**filter_condition)



# check user's auth to comment for review, reply(edit), and deltet
def check_reviewship_exist(comment, user):
    reviewships = Reviewship.objects.filter(comment=comment, user=user)
    reviewship_count = len(reviewships)
    if reviewship_count > 1:
        reviewships.delete()
        return None
    elif reviewship_count == 1:
        return reviewships[0]
    else:
        return None

def check_review_auth(comment, user):
    if comment.author == user:
        return (False, False)
    reviewship = check_reviewship_exist(comment, user)
    if reviewship is not None:
        useful_available = bool(not reviewship.is_useful)
        unuseful_available = reviewship.is_useful
        return (useful_available, unuseful_available)
    else:
        return (True, True)

def check_reply_auth(user):
    return bool(user.is_superuser)
    
def check_delete_auth(comment, user):
    return user.is_superuser or (user.is_authenticated and (comment.author == user))

def check_comment_auth(comment, user):
    auth = {'useful': False,'unuseful': False,'edit': False,'delete': False}
    auth['useful'], auth['unuseful'] = check_review_auth(comment, user)
    auth['edit'] = check_reply_auth(user)
    auth['delete'] = check_delete_auth(comment, user)
    return auth


def get_comment(comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
    except:
        raise Http404()
    return comment

def create_reviewship(user, comment, is_useful):
    new_reviewship = Reviewship(
        user=user,
        comment=comment,
        is_useful=is_useful)
    new_reviewship.save()

