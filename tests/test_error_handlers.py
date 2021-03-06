import unittest
from unittest.mock import patch

from response_operations_social_ui import create_app


class TestErrorHandlers(unittest.TestCase):
    def setUp(self):
        app = create_app('TestingConfig')
        self.app = app.test_client()

    @patch('requests.post')
    def test_exception_error_page(self, mock_post):
        mock_post.side_effect = Exception("error")
        response = self.app.post('/sign-in', data={'username': 'username', 'password': 'password'},
                                 follow_redirects=True)
        self.assertIn(b'Something has gone wrong with the website.', response.data)
