from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from deltago.exceptions import errors

from deltago.models import Comment

from deltago.views.services.comments import get_comments, creat_comment, review_comment

def comments(request):
    page = request.GET.get('page', 1)
    data = get_comments(page, 20)
    return render(request, 'deltago/comments/comments.html', data)

# login required
def add_comment(request):
    # user = request.user
    user = User.objects.get(pk=1)
    if request.method == "POST":
        content = request.POST.get('content')
        nickname = request.POST.get('nickname')
        is_public = request.POST.get('is_public', False)
        new_comment = creat_comment(user, content, nickname, is_public)
        return redirect('comments')
    else:
        return render(request, 'deltago/comments/add_comment.html')

# login required
def review(request, comment_id, is_useful):
    # user = request.user
    user = User.objects.get(pk=1)
    try:
        comment = Comment.objects.get(pk=comment_id)
        review_comment(user, comment, int(is_useful))
    except ObjectDoesNotExist as e:
        print e
    except errors.DuplicateError as e:
        print e
    return redirect('comments')

