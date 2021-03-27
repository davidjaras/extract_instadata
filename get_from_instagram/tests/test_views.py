import unittest
from django.test import Client


class SimpleTest(unittest.TestCase):
    ''' Test user interactions and system responses.'''

    def setUp(self):
        self.client = Client()

    def test_index(self):
        '''
        Given a GET request to index 
        When no params is passed
        Then must return the page with context equals to None
        '''

        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context is None
        self.assertEqual(response.context['results'], None)
    
    def test_index_with_param(self):
        '''
        Given a GET request to index 
        When searcher param
        Then must return the page with context equals a dict type
        '''

        # Issue a GET request.
        response = self.client.get('/', {'searcher': 'juliankag'})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 5 customers.
        self.assertIsInstance(response.context['results'], dict)