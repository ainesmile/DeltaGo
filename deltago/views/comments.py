from django.shortcuts import render
from django.contrib.auth.models import User



from deltago.views.services.comments import get_comments

def comments(request):
    page = request.GET.get('page', 1)
    data = get_comments(page, 20)
    return render(request, 'deltago/comments/comments.html', data)

