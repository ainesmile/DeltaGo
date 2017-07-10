from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.apps import apps
from deltago.models.search import Search
from deltago.models.commodity import BabyCare

def pagination(items, page, paginate_by):
    paginator = Paginator(items, paginate_by)
    try:
        text = paginator.page(page)
    except PageNotAnInteger:
        text = paginator.page(1)
    except EmptyPage:
        text = paginator.page(paginator.num_pages)
    return text

def search(content):
    results = []
    search_filters = Search.objects.filter(name__contains=content)
    for item in search_filters:
        stockcode = item.stockcode
        model_name = item.model_name
        app_model = apps.get_model(app_label='deltago', model_name=model_name)
        list = app_model.objects.filter(stockcode=stockcode)
        if len(list) != 0:
            results.append(list[0])
    return results
