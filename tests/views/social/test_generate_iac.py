import requests_mock

from tests.views.social import SocialViewTestCase


class TestGenerateIac(SocialViewTestCase):

    @requests_mock.mock()
    def test_generate_iac(self, mock_request):
        post_data = {"case_id": self.case_id}

        mock_request.post(self.iac_url, json=self.mocked_iac)
        mock_request.get(self.iac_url, json=self.mocked_iacs)
        mock_request.get(self.get_case_by_id_url, json=self.mocked_case_details)
        mock_request.get(self.get_sample_by_id_url, json=self.mocked_sample_attributes)
        mock_request.get(self.get_case_events_by_case_id_url, json=self.mocked_case_events)
        mock_request.get(self.get_available_case_group_statuses_direct_url, json=self.mocked_case_group_statuses)

        response = self.client.post(f'/iac', follow_redirects=True, data=post_data)

        self.assertIn("k7j6n7pffg8g".encode(), response.data)
        self.assertIn("16 unique".encode(), response.data)
