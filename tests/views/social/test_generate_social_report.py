import requests_mock

from tests.views.social import SocialViewTestCase


class TestGenerateSocialReport(SocialViewTestCase):

    @requests_mock.mock()
    def test_generate_social_mi(self, mock_request):
        mock_request.get(self.get_social_mi_report)
        response = self.client.get(f'/response_chasing', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

