import requests
import os
from json.decoder import JSONDecodeError


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
        except JSONDecodeError as e:
            results['error'] = 'Response is not json type'
        finally:
            return results
    return None


def extract_user_data(json_res):
    data = {}

    try:
        data['username'] = json_res['graphql']['user']['username']
        data['full_name'] = json_res['graphql']['user']['full_name']
        data['instagram_id'] = json_res['graphql']['user']['id']
        data['followers'] = json_res['graphql']['user']['edge_followed_by']
        data['following'] = json_res['graphql']['user']['edge_follow']
        data['is_private'] = json_res['graphql']['user']['is_private']
    except KeyError as e:
        data['error'] = ('Bad response by source. '
                         'Json response does not have the correct fields.')

    return data


def get_instagram_user_posts(username):
    cmd = f'instagram-scraper --media-metadata {username} -d media/{username}'
    os.system(cmd)


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
