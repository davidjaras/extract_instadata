from get_from_instagram import functions
from unittest import TestCase
from .mock_request_response import get_mock_data


class TestRequestData(TestCase):

    def test_extract_user_data(self):
        self.mock_data = get_mock_data()

        self.assertIsInstance(functions.extract_user_data({}), dict)
        self.assertIn('error', functions.extract_user_data({}))
        self.assertIn('username', functions.extract_user_data(self.mock_data))
        self.assertIn('instagram_id', functions.extract_user_data(self.mock_data))
        self.assertIn('full_name', functions.extract_user_data(self.mock_data))
        self.assertIn('followers', functions.extract_user_data(self.mock_data))
        self.assertIn('following', functions.extract_user_data(self.mock_data))
        self.assertIn('is_private', functions.extract_user_data(self.mock_data))
