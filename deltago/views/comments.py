from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from deltago.views.services.comments import get_comments, creat_comment

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
