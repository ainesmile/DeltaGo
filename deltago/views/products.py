from django.shortcuts import render, redirect

from deltago.views.services.products import sub

def sub_category(request, categ_name, sub_name):
    # condition = {
    #     'category': categ_name,
    #     'sub_category': sub_name
    # }
    page = request.GET.get("page", 1)
    data = sub(categ_name, sub_name, page, 20)
    return render(request, 'deltago/commodity/base.html', data)