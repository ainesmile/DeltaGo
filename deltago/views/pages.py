from django.shortcuts import render, redirect
from services.share import pagination, search_results
from deltago.forms import SearchForm


def index(request):
    return render(request, 'deltago/index.html')

def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            content = form.cleaned_data["content"]
            content = str(content)
            results = search_results(content)
            page = request.GET.get('page', 1)
            per_page = 20
            data = pagination(results, page, per_page)
            return render(request, 'deltago/share/search_result.html', {
                "products": data,
                "paginations": data
                })
    return redirect('index')
        
