from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve
import urlparse

from deltago.exceptions import errors

from deltago.models import Comment

from deltago.views.services.comments import get_comments, creat_comment, review_comment

def comments(request):
    page = request.GET.get('page', 1)
    data = get_comments(page, 20)
    return render(request, 'deltago/comments/comments.html', data)

@login_required(login_url='login', redirect_field_name='next')
def add_comment(request):
    user = request.user
    if request.method == "POST":
        content = request.POST.get('content')
        nickname = request.POST.get('nickname')
        is_public = request.POST.get('is_public', False)
        new_comment = creat_comment(user, content, nickname, is_public)
        return redirect('comments')
    else:
        return render(request, 'deltago/comments/add_comment.html')

@login_required(login_url='login')
def review(request, comment_id, is_useful):
    user = request.user
    try:
        comment = Comment.objects.get(pk=comment_id)
        review_comment(user, comment, int(is_useful))
    except ObjectDoesNotExist as e:
        print e
    except errors.DuplicateError as e:
        print e
    return redirect('comments')

@login_required(login_url='login')
def delete_comment(request, comment_id):
    next_view = request.GET.get('next_view', 'index')
    comment = Comment.objects.get(pk=comment_id)
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




