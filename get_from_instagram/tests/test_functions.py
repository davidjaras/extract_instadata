# Python
from unittest import TestCase

# Project
from get_from_instagram import functions as f
from .mock_request_response import get_mock_data


class TestFunctions(TestCase):

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
