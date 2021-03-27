# Django
from django.shortcuts import render

# Python
import requests

# Project
from .functions import get_instagram_user_data, get_instagram_user_posts


def index_get_from_instagram(request):
    searcher = request.GET.get('searcher')

    results = get_instagram_user_data(searcher)

    if results is not None:
        if(results.get('is_private') is False):
            posts = get_instagram_user_posts(results.get('username'))
    
    return render(request, 'get_from_instagram/index.html', {'results': results})
