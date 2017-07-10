from django import forms

from deltago.models.search import Search

class SearchForm(forms.Form):
    content = forms.CharField(max_length=128)