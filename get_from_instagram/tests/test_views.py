# Django
from django.test import TestCase, Client

# Python
import unittest

# Project
from get_from_instagram.models import InstagramUser, InstagramPost, Media


class ViewsTest(unittest.TestCase):
    ''' Test user interactions and system responses.'''
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = InstagramUser.objects.create(
            id=1,
            username='testing',
            full_name='Test Admetricks',
            instagram_id=123456789,
            followers=1000000,
            following=10
        )

        post = InstagramPost.objects.create(
            post_id=123456789,
            caption='Test Admetricks',
            pub_date=datetime.now(),
            likes_amount=1000000,
            comments_amount=10,
            views_amount=0,
            instagram_user=user
        )

        Media.objects.create(
            url='test.sourcemedia.com/test/image/image1.jpg',
            local_path='.media/test/image/image1.jpg',
            is_video=False,
            instagram_post=post,
            instagram_user=user
        )

    def setUp(self):
        self.client = Client()

    def test_index(self):
        '''
        Given a GET request to index
        When no params is passed
        Then must return the page with success = False
        '''
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['success'], False)

    def test_index_with_param(self):
        '''
        Given a GET request to index
        When searcher param and it exists in instagram
        Then must return the page with success = True
        '''
        response = self.client.get('/', {'searcher': 'davidjaras'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['success'], True)

    def test_index_with_wrong_param(self):
        '''
        Given a GET request to index
        When searcher param and it doesn't exists in instagram
        Then must return the page with success = False
        '''
        response = self.client.get('/', {'searcher': ''})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['success'], False)

    def test_details(self):
        '''
        Given a GET request to details
        When id params does not exists
        Then must return the page with code 404
        '''
        response = self.client.get(f'/details/{1}')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['posts'], list)
        self.assertIsInstance(response.context['instagram_user'], dict)

    def test_details_404(self):
        '''
        Given a GET request to details
        When id params does not exists
        Then must return the page with code 404
        '''
        response = self.client.get(f'/details/{12}')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['posts'], list)
        self.assertIsInstance(response.context['instagram_user'], dict)
        self.assertIn('error', response.context['instagram_user'])
