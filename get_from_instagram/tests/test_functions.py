# Python
from django.test import TestCase
from datetime import datetime

# Project
from get_from_instagram import functions as f
from .mock_request_response import get_mock_data
from get_from_instagram.models import InstagramUser, InstagramPost, Media


class TestFunctions(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = InstagramUser.objects.create(
            username='testing',
            full_name='Test Admetricks',
            instagram_id=123456789,
            followers=1000000,
            following=10,
            is_private=False
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

    def test_clean_searcher(self):
        # Given a username must return clean whitespaces and quit @
        self.assertEqual(f.clean_searcher('@   username   '), 'username')
        # Given a None input return None
        self.assertIsNone(f.clean_searcher(None))
        # Given a empty string '', must return None
        self.assertIsNone(f.clean_searcher(''))

    def test_get_instagram_user_data(self):
        # given no param return None
        self.assertEqual(f.get_instagram_user_data(), (None, None))

    def test_get_instagram_user_posts(self):
        # Given a instagram user input with is_private == True
        # Return empty dict and error
        instagram_user = {'username': 'testing', 'is_private': True}
        posts, error = f.get_instagram_user_posts(instagram_user, None)
        self.assertEqual(posts, {})
        self.assertIsNone(error)

        # Given a empty instagram user input
        # Return a None element and a string error
        instagram_user = {}
        posts, error = f.get_instagram_user_posts(instagram_user, None)
        self.assertIsNone(posts)
        self.assertIsInstance(error, str)

    def test_extract_user_data(self):
        self.mock_data = get_mock_data()

        # given no data return a dict
        self.assertIsInstance(f.extract_user_data({}), dict)

        # Given no data return a dict with an element called error
        self.assertIn('error', f.extract_user_data({}))

        # Given a correct input return correct instagram user fields
        self.assertIn('username', f.extract_user_data(self.mock_data))
        self.assertIn('instagram_id', f.extract_user_data(self.mock_data))
        self.assertIn('full_name', f.extract_user_data(self.mock_data))
        self.assertIn('followers', f.extract_user_data(self.mock_data))
        self.assertIn('following', f.extract_user_data(self.mock_data))
        self.assertIn('is_private', f.extract_user_data(self.mock_data))

    def test_save_user_info(self):
        # Given a new user must return a InstagramUser instance
        mock_user = {
            'username': 'testing2',
            'full_name': 'Test Test',
            'instagram_id': 123456789,
            'followers': 1000000,
            'following': 10
        }
        instagram_user = f.save_user_info(mock_user)
        self.assertIsInstance(instagram_user, InstagramUser)

        # Given a user that already exist must return a InstagramUser instance
        mock_user = {
            'username': 'testing',
            'full_name': 'Test Test',
            'instagram_id': 1234567890,
            'followers': 1000000,
            'following': 10,
            'is_private': False
        }
        instagram_user = f.save_user_info(mock_user)
        self.assertIsInstance(instagram_user, InstagramUser)

        # Given a user that already exist with updated data
        # must return a updated instance except instagram_id
        mock_user = {
            'username': 'testing',
            'full_name': 'Test Test Test',
            'instagram_id': 987654321,
            'followers': 9999,
            'following': 99,
            'is_private': True
        }
        old_user = InstagramUser.objects.get(id=1)
        new_user = f.save_user_info(mock_user)
        self.assertNotEqual(old_user.full_name, new_user.full_name)
        self.assertNotEqual(old_user.followers, new_user.followers)
        self.assertNotEqual(old_user.following, new_user.following)
        self.assertNotEqual(old_user.is_private, new_user.is_private)
        self.assertEqual(old_user.instagram_id, new_user.instagram_id)

    def test_save_post_info(self):
        # Given a new post must return a InstagramPost instance
        # and is_new_data = True
        instagram_user = InstagramUser.objects.get(id=1)
        mock_post = {
            'post_id': 1234567892,
            'caption': 'Test Admetricks',
            'pub_date': datetime.now(),
            'likes_amount': 1000000,
            'comments_amount': 10,
            'views_amount': 0,
            'instagram_user': instagram_user
        }

        instagram_post, is_new_data = f.save_post_info(mock_post)
        self.assertIsInstance(instagram_post, InstagramPost)
        self.assertTrue(is_new_data)

        # Given a post that already exist must return a InstagramPost instance
        # and is_new_data = False
        instagram_user = InstagramUser.objects.get(id=1)
        mock_post = {
            'post_id': 123456789,
            'caption': 'Test Admetricks',
            'pub_date': datetime.now(),
            'likes_amount': 1000000,
            'comments_amount': 10,
            'views_amount': 0,
            'instagram_user': instagram_user
        }

        instagram_post, is_new_data = f.save_post_info(mock_post)
        self.assertIsInstance(instagram_post, InstagramPost)
        self.assertFalse(is_new_data)

        # Given a post that already exist with updated data
        # must return a updated instance except post_id and is_new_data = false
        mock_post = {
            'post_id': 123456789,
            'caption': 'Test Test',
            'pub_date': datetime.now(),
            'likes_amount': 555,
            'comments_amount': 555,
            'views_amount': 88,
            'instagram_user': instagram_user
        }
        old_post = InstagramPost.objects.get(post_id=123456789)
        new_post, is_new_data = f.save_post_info(mock_post)
        self.assertFalse(is_new_data)
        self.assertNotEqual(old_post.caption, new_post.caption)
        self.assertNotEqual(old_post.likes_amount, new_post.likes_amount)
        self.assertNotEqual(old_post.comments_amount, new_post.comments_amount)
        self.assertNotEqual(old_post.views_amount, new_post.views_amount)
        self.assertEqual(old_post.post_id, new_post.post_id)
        self.assertEqual(old_post.pub_date, new_post.pub_date)
        self.assertEqual(old_post.instagram_user, new_post.instagram_user)
