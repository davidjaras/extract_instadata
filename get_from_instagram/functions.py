import requests
import os
import re
from json.decoder import JSONDecodeError
from django.conf import settings
import json
from datetime import datetime
from .models import InstagramUser, InstagramPost, Media


def get_instagram_user_data(search):
    results = {}
    if search is not None:
        try:
            url = f'https://www.instagram.com/{search}/?__a=1'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
                'accept': 'application/json'
            }
            response = requests.get(url, headers=headers).json()
            results = extract_user_data(response)
        except JSONDecodeError:
            results['error'] = 'Response is not json type'
        except ConnectionError:
            results['error'] = 'Error trying to connect with Instagram.'
        finally:
            return results
    return None


def extract_user_data(json_res):
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


def get_instagram_user_posts(username):
    cmd = f'instagram-scraper --media-metadata {username} -d media/{username}'
    os.system(cmd)
    path = f'media/{username}/{username}.json'
    posts = extract_post_data(path)
    return posts


def extract_post_data(path):
    data = read_json(path)
    posts = {'posts': []}

    try:
        for data_post in data['GraphImages']:
            post = {}

            try:
                post['post_id'] = data_post['id']
                pre_caption = str(data_post['edge_media_to_caption']['edges'])
                post['caption'] = (pre_caption.replace("[{'node': {'text': '", "")
                                            .replace("'}}]", ""))
                post['pub_date'] =  datetime.fromtimestamp(data_post['taken_at_timestamp'])
                post['likes_amount'] = data_post['edge_media_preview_like']['count']
                post['comments_amount'] = data_post['edge_media_to_comment']['count']
                post['views_amount'] = data_post.get('video_view_count')
                post['urls'] = data_post['urls']

                posts['posts'].append(post)
            except Exception:
                pass  # Not append if an error happens 
            
    except KeyError as e:
        posts['error'] = ('Bad response by posts source. '
                         'Json response does not have the correct fields.')
    
    return posts


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


def save_in_database(user, posts):

    # save instagram user data
    instagram_user = InstagramUser.objects.create(**user)
    instagram_user.save()

    # save posts related to instagram user data
    for post in posts:
        urls = post['urls']
        post.pop('urls')
        post['instagram_user'] = instagram_user
        instagram_post = InstagramPost.objects.create(**post)
        instagram_post.save()

        for url in urls:
            is_video = False
            filename = re.findall(r'/\w*\.[jm][p][g4]', url)[0]
            ext = filename[-3:]  # last 3 caracters that contains extention

            if ext == 'mp4':
                is_video = True

            local_path = f'media/{instagram_user.username}{filename}'
            instagram_post.media_set.create(url=url,
                                            local_path=local_path,
                                            is_video=is_video,
                                            instagram_user=instagram_post.instagram_user)
    
    return True

