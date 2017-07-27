from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def pagination(items, page, paginate_by):
    paginator = Paginator(items, paginate_by)
    try:
        text = paginator.page(page)
    except PageNotAnInteger:
        text = paginator.page(1)
    except EmptyPage:
        text = paginator.page(paginator.num_pages)
    return text
