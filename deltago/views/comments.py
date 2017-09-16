# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, SuspiciousOperation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve
import urlparse

from deltago.exceptions import errors

from deltago.models import Comment, Reply

from deltago.views.services import comment_service

def comments(request):
    page = request.GET.get('page', 1)
    data = comment_service.get_comments(request.user, page, 20)
    return render(request, 'deltago/comments/comments.html', data)

@login_required(login_url='login', redirect_field_name='next')
def add_comment(request):
    user = request.user
    if request.method == "POST":
        content = request.POST.get('content')
        nickname = request.POST.get('nickname')
        is_public = not bool(request.POST.get('keep_private'))
        new_comment = comment_service.create_comment(user, content, nickname, is_public)
        return redirect('my_comments')
    else:
        return render(request, 'deltago/comments/add_comment.html')

@login_required(login_url='login')
def review(request, comment_id, is_useful):
    user = request.user
    try:
        comment = Comment.objects.get(pk=comment_id)
        comment_service.review(user, comment, int(is_useful))
    except ObjectDoesNotExist as e:
        raise Http404('该留言不存在。')
    except errors.DuplicateError as e:
        raise SuspiciousOperation(e)
    except errors.OperationError as e:
        raise SuspiciousOperation(e)
    return redirect('comments')

@login_required(login_url='login')
def delete_comment(request, comment_id):
    next_view = request.GET.get('next_view', 'index')
    try:
        comment = Comment.objects.get(pk=comment_id)
    except ObjectDoesNotExist as e:
        raise Http404('该留言不存在。')
    if request.method == 'POST':
        comment.delete()
        return redirect(next_view)
    else:
        referer = request.META.get('HTTP_REFERER', '/')
        parse_result = urlparse.urlparse(referer)
        next_view = resolve(parse_result.path).url_name
    return render(request, 'deltago/comments/delete_comment.html', {
        "comment": comment,
        "next_view": next_view})

@login_required(login_url='login')
def reply_comment(request, comment_id):
    user = request.user
    if not user.is_superuser:
        raise PermissionDenied
    try:
        comment = Comment.objects.get(pk=comment_id)
    except ObjectDoesNotExist:
        raise Http404('该留言不存在。')
    if request.method == 'POST':
        content = request.POST.get('content')
        keep_private = request.POST.get('keep_private')
        comment_service.create_reply(user, comment, content, keep_private)
        replies = Reply.objects.filter(author=user)
        return redirect('comments')
    else:
        return render(request, 'deltago/comments/reply_comment.html', {
            "comment": comment})

@login_required(login_url='login')
def my_comments(request):
    user = request.user
    page = request.GET.get('page', 1)
    render_data = comment_service.get_user_comments(user, page, 20)
    return render(request, 'deltago/comments/my_comments.html', render_data)
