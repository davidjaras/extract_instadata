# Django
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

# Python
import requests

# Project
import get_from_instagram.functions as f
from .models import InstagramUser, InstagramPost, Media


def index_get_from_instagram(request):
    '''
    Index page view.
    Depending on the request search profile online or in database.
    '''
    searcher = request.GET.get('searcher')
    error = None
    user = None
    posts = None
    success = False

    instagram_user, error = f.get_instagram_user_data(searcher)

    if instagram_user is not None:
        posts, error = f.get_instagram_user_posts(instagram_user)

    if posts is not None:
        success, error = f.save_in_database(instagram_user, posts)

    if success:
        instagram_user_id = instagram_user.get('instagram_id')
        user = InstagramUser.objects.get(instagram_id=instagram_user_id)

    return render(request,
                  'get_from_instagram/index.html',
                  {'success': success,
                   'user': user,
                   'error': error})


def get_details(request, instagram_user_id=None):
    '''
    Detail page view.
    Depending on the request instagram_user_id get data from database.
    '''
    posts = []
    instagram_user = {}
    try:
        instagram_user = InstagramUser.objects.get(pk=instagram_user_id)
        posts = Media.objects.filter(instagram_user=instagram_user_id)
    except InstagramUser.DoesNotExist:
        instagram_user['error'] = 'Instagram user not found.'
    else:
        paginator = Paginator(posts, 30)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

    return render(request,
                  'get_from_instagram/details.html',
                  {'posts': posts, 'instagram_user': instagram_user})
