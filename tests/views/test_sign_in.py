import jwt
import requests_mock

from config import TestingConfig
from response_operations_social_ui import create_app
from tests.views.social import SocialViewTestCase

url_sign_in_data = f'{TestingConfig.UAA_SERVICE_URL}/oauth/token'


class TestSignIn(SocialViewTestCase):

    def setUp(self):
        payload = {'user_id': 'test-id',
                   'aud': 'response_operations_social'}

        app = create_app('TestingConfig')
        key = app.config['UAA_PUBLIC_KEY']

        self.access_token = jwt.encode(payload, key=key)
        self.client = app.test_client()

    def test_sign_in_page(self):
        response = self.client.get('/sign-in')
        self.assertIn(b'Username', response.data)
        self.assertIn(b'Password', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Sign out", response.data)

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You are now signed out', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Sign out", response.data)

    @requests_mock.mock()
    def test_sign_in(self, mock_request):
        mock_request.post(url_sign_in_data, json={"access_token": self.access_token.decode()}, status_code=201)

        response = self.client.post("/sign-in", follow_redirects=True,
                                    data={"username": "user", "password": "pass"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("Find case by postcode".encode(), response.data)
        self.assertIn("Sign out".encode(), response.data)

    @requests_mock.mock()
    def test_sign_in_unable_to_decode_token(self, mock_request):
        mock_request.post(url_sign_in_data, json={"access_token": 'invalid'}, status_code=201)

        response = self.client.post("/sign-in", follow_redirects=True,
                                    data={"username": "user", "password": "pass"})

        request_history = mock_request.request_history
        self.assertEqual(len(request_history), 1)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error 500 - Server error', response.data)

    @requests_mock.mock()
    def test_fail_authentication(self, mock_request):
        mock_request.post(url_sign_in_data, status_code=401)

        response = self.client.post("/sign-in", follow_redirects=True,
                                    data={"username": "user", "password": "wrong"})

        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Incorrect username or password', response.data)

    @requests_mock.mock()
    def test_fail_authentication_missing_token(self, mock_request):
        mock_request.post(url_sign_in_data, json={}, status_code=201)  # No token in response

        response = self.client.post("/sign-in", follow_redirects=True,
                                    data={"username": "user", "password": "wrong"})

        self.assertEqual(response.status_code, 200)

        self.assertIn(b'Incorrect username or password', response.data)

    @requests_mock.mock()
    def test_fail_server_error(self, mock_request):
        mock_request.post(url_sign_in_data, status_code=500)

        response = self.client.post("/sign-in", follow_redirects=True,
                                    data={"username": "user", "password": "pass"})

        request_history = mock_request.request_history
        self.assertEqual(len(request_history), 1)
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error 500 - Server error', response.data)

    @requests_mock.mock()
    def test_sign_in_redirect_while_authenticated(self, mock_request):
        mock_request.post(url_sign_in_data, json={"access_token": self.access_token.decode()}, status_code=201)

        response = self.client.post("/sign-in", follow_redirects=True,
                                    data={"username": "user", "password": "pass"})

        self.assertIn("Find case by postcode".encode(), response.data)

        # First test that we hit a redirect
        response = self.client.get('/sign-in')
        self.assertEqual(response.status_code, 302)

        # Then test that the redirect takes you to the home page.
        response = self.client.get('/sign-in', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Find case by postcode".encode(), response.data)

    @requests_mock.mock()
    def test_sign_in_next_url(self, mock_request):
        # Given
        mock_request.get(self.get_case_by_id_url, json=self.mocked_case_details)
        mock_request.get(self.get_sample_attributes_by_id_url, json=self.mocked_sample_attributes)
        mock_request.get(self.get_case_events_by_case_id_url, json=self.mocked_case_events)
        mock_request.get(self.iac_url, json=self.mocked_iacs)
        mock_request.get(self.get_available_case_group_statuses_direct_url, json=self.mocked_case_group_statuses)
        mock_request.get(self.get_collection_exercise_events_by_id_url, json=self.mocked_collex_events)
        with self.client.session_transaction() as session:
            session['next'] = f'/case/{self.case_id}'
        mock_request.post(url_sign_in_data, json={"access_token": self.access_token.decode()}, status_code=201)

        # When
        response = self.client.post("/sign-in", follow_redirects=True,
                                    data={"username": "user", "password": "pass"})

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Find case by postcode', response.data)
        self.assertIn(self.mocked_sample_attributes['attributes']['ADDRESS_LINE1'].encode(), response.data)
        self.assertIn(self.mocked_sample_attributes['attributes']['ADDRESS_LINE2'].encode(), response.data)
        self.assertIn(self.mocked_sample_attributes['attributes']['LOCALITY'].encode(), response.data)
        self.assertIn(self.mocked_sample_attributes['attributes']['TOWN_NAME'].encode(), response.data)
        self.assertIn(self.mocked_sample_attributes['attributes']['POSTCODE'].encode(), response.data)
        self.assertIn(self.mocked_sample_attributes['attributes']['TLA'].encode(), response.data)
        self.assertIn(self.mocked_sample_attributes['attributes']['REFERENCE'].encode(), response.data)

    def test_sign_out_deleting_session_variables(self):
        with self.client.session_transaction() as session:
            session['next'] = f'/case/{self.case_id}'
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You are now signed out', response.data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Sign out", response.data)
        with self.client.session_transaction() as session:
            self.assertEqual(session.get("next"), None)
