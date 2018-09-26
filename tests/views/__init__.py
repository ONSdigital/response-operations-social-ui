from unittest import TestCase

from response_operations_social_ui import create_app


class ViewTestCase(TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
