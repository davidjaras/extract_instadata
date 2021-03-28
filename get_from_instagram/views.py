# Django
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

# Python
import requests

# Project
from .functions import get_instagram_user_data, get_instagram_user_posts, save_in_database
from .models import InstagramUser, InstagramPost, Media


def index_get_from_instagram(request):
    searcher = request.GET.get('searcher')
    posts = []
    success = False
    user = ""

    instagram_user = get_instagram_user_data(searcher)
    #instagram_user = {'username': 'davidjaras', 'full_name': 'David Jaramillo S', 'instagram_id': '1944345247', 'followers': 176, 'following': 252, 'is_private': False} # DELETE THIS LINE

    if instagram_user is not None:
        if(instagram_user.get('is_private') is False):
            posts = get_instagram_user_posts(instagram_user.get('username'))
            success = save_in_database(instagram_user, posts.get('posts'))
    
    if success:
        user = InstagramUser.objects.get(instagram_id=instagram_user.get('instagram_id'))
    
    return render(request, 'get_from_instagram/index.html',
                    {'instagram_user': instagram_user, 'posts': posts, 'success': success, 'user':user})


def get_details(request, instagram_user_id):
    posts = []
    
    try:
        if instagram_user_id is not None:
            instagram_user = InstagramUser.objects.get(pk=instagram_user_id)
            posts = Media.objects.filter(instagram_user=instagram_user_id)
            paginator = Paginator(posts, 21)

            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)

            return render(request, 'get_from_instagram/details.html', {'posts':posts, 'instagram_user':instagram_user})
    except InstagramPost.DoesNotExist:
        raise Http404("Post does not exist")

    return redirect(request, 'get_from_instagram/index.html')
