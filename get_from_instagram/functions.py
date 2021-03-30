# Django
from django.db.utils import IntegrityError

# Python
import os
import re
import json
import requests
from datetime import datetime
from json.decoder import JSONDecodeError

# Project
from get_from_instagram.vars import URL, HEADERS
from .models import InstagramUser, InstagramPost, Media


''' Views Functions. '''


def clean_searcher(searcher):
    if searcher is None or searcher == '':
        return None

    searcher = searcher.replace('@', '')
    searcher = searcher.strip().lower()

    return searcher


def get_instagram_user_data(search=None, error=None):
    '''
    Make the request to Instagram and return a json response.
    If something is wrong return 'error'.
    If username doesn´t exists return None.
    '''
    results = {}
    if search is not None:
        try:
            url = URL.replace('$username$', search)
            response = requests.get(url, headers=HEADERS).json()
            results = extract_user_data(response)
        except JSONDecodeError:
            error = 'Response is not json type'
        except ConnectionError:
            error = 'Error trying to connect with Instagram.'
        finally:
            return results, error
    return None, None


def get_instagram_user_posts(instagram_user, error=None):
    '''
    Funtion to download Instagram user's posts.
    This create a json file with data related to posts.
    '''
    try:
        if instagram_user.get('is_private') is False:
            usern = instagram_user.get('username')

            cmd = f'instagram-scraper {usern} --media-metadata --latest -d media/{usern}'
            os.system(cmd)
            path = f'media/{usern}/{usern}.json'

            posts, error = extract_post_data(path)
            return posts, error

        elif instagram_user.get('is_private') is True:
            return {}, error

        else:
            return None, 'Get user data failed. Verify account exist.'
    except Exception:
        return None, 'something went wrong. Collect posts data failed.'


def save_in_database(user, posts={}, error=None):
    '''
    Function to save in Database instagram user data.
    Format variables and storage.
    '''
    try:
        instagram_user = save_user_info(user)
    except Exception:
        error = 'Unable to save user in database.'
        return False, error

    try:
        if posts.get('posts') is not None:
            for post in posts.get('posts'):
                urls = post['urls']
                post.pop('urls')
                post['instagram_user'] = instagram_user
                instagram_post, new_data = save_post_info(post)
                if new_data:
                    save_media(urls, instagram_user, instagram_post)
    except Exception:
        error = 'Unable to save posts in database.'
        return False, error

    return True, error


''' Internal functions that supports Views Functions. '''


def extract_user_data(json_res):
    '''
    Funtion to filter and format instagram user data.
    Return a new dictionary with the importat field for this app.
    '''
    data = {}

    try:
        data_user = json_res['graphql']['user']
        data['username'] = data_user['username']
        data['full_name'] = data_user['full_name']
        data['instagram_id'] = data_user['id']
        data['followers'] = data_user['edge_followed_by']['count']
        data['following'] = data_user['edge_follow']['count']
        data['is_private'] = data_user['is_private']
    except KeyError as e:
        data['error'] = ('Bad response by source. '
                         'Json response does not have the correct fields.')

    return data


def extract_post_data(path, error=None):
    '''
    Funtion to filter and format instagram posts data.
    Return a new dictionary with the importat field for this app.
    '''
    data = read_json(path)
    posts = {'posts': []}

    try:
        for data_post in data['GraphImages']:
            post = {}

            post['post_id'] = data_post['id']
            pre_caption = str(data_post['edge_media_to_caption']['edges'])
            post['caption'] = (pre_caption
                               .replace("[{'node': {'text': '", "")
                               .replace("'}}]", ""))
            post['pub_date'] = datetime.fromtimestamp(
                                    data_post['taken_at_timestamp']
                                )
            post['likes_amount'] = (
                data_post['edge_media_preview_like']['count']
            )
            post['comments_amount'] = (
                data_post['edge_media_to_comment']['count']
            )
            post['views_amount'] = data_post.get('video_view_count')
            post['urls'] = data_post['urls']

            posts['posts'].append(post)

    except KeyError as e:
        error = ('Bad response by posts source. '
                 'Json response does not have the correct fields.')
        return {}, error

    return posts, error


def read_json(filename):
    ''' Read json file specified in filename param. '''
    if type(filename) not in [str]:
        return TypeError('File name must be a string')
    try:
        with open(filename, 'r') as file:
            settings = json.load(file)
        return settings
    except Exception as e:
        return e


def save_user_info(user):
    '''Save instagram user data.'''
    try:
        instagram_user = InstagramUser.objects.get(username=user['username'])
        instagram_user.full_name = user['full_name']
        instagram_user.followers = user['followers']
        instagram_user.following = user['following']
        instagram_user.is_private = user['is_private']

    except InstagramUser.DoesNotExist:
        instagram_user = InstagramUser.objects.create(**user)

    finally:
        instagram_user.save()

    return instagram_user


def save_post_info(post):
    '''Save instagram post data.'''
    is_new_data = True

    try:
        instagram_post = InstagramPost.objects.get(post_id=post['post_id'])
        instagram_post.caption = post['caption']
        instagram_post.likes_amount = post['likes_amount']
        instagram_post.comments_amount = post['comments_amount']
        instagram_post.views_amount = post['views_amount']
        is_new_data = False

    except InstagramPost.DoesNotExist:
        instagram_post = InstagramPost.objects.create(**post)

    finally:
        instagram_post.save()

    return instagram_post, is_new_data


def save_media(urls, instagram_user, instagram_post):
    '''Save instagram post data.'''
    for url in urls:
        is_video = False
        filename = re.findall(r'/\w*\.[jm][p][g4]', url)[0]

        # validate file extension
        ext = filename[-3:]  # last 3 caracters that contains extension
        if ext == 'mp4':
            is_video = True

        local_path = f'media/{instagram_user.username}{filename}'
        instagram_post.media_set.create(
            url=url,
            local_path=local_path,
            is_video=is_video,
            instagram_user=instagram_post.instagram_user
        )
    return 'Done'
