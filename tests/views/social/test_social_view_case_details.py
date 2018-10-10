from collections import OrderedDict
import json

import requests_mock

from response_operations_social_ui.views.social.social_view_case_details import group_and_order_events
from tests.views.social import SocialViewTestCase


class TestSocialViewCaseDetails(SocialViewTestCase):

    @requests_mock.mock()
    def test_get_social_case(self, mock_request):
        mock_request.get(self.get_case_by_id_url, json=self.mocked_case_details)
        mock_request.get(self.get_sample_attributes_by_id_url, json=self.mocked_sample_attributes)
        mock_request.get(self.get_case_events_by_case_id_url, json=self.mocked_case_events)
        mock_request.get(self.iac_url, json=self.mocked_iacs)
        mock_request.get(self.get_available_case_group_statuses_direct_url, json=self.mocked_case_group_statuses)

        response = self.client.get(f'/case/{self.case_id}', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("LMS0001".encode(), response.data)
        self.assertIn("NV184QG".encode(), response.data)
        self.assertIn("In progress".encode(), response.data)

    @requests_mock.mock()
    def test_get_social_sample_attributes_fail(self, mock_request):
        mock_request.get(self.get_case_by_id_url, json=self.mocked_case_details)
        mock_request.get(self.get_sample_attributes_by_id_url, status_code=500)
        mock_request.get(self.iac_url, json=self.mocked_iacs)

        response = self.client.get(f'/case/{self.case_id}', follow_redirects=True)

        request_history = mock_request.request_history
        self.assertEqual(len(request_history), 2)
        self.assertEqual(response.status_code, 500)

    @requests_mock.mock()
    def test_update_case_status_view(self, mock_request):
        mock_request.get(self.get_case_by_id_url, json=self.mocked_case_details)
        mock_request.get(self.get_sample_attributes_by_id_url, json=self.mocked_sample_attributes)
        mock_request.get(self.get_case_events_by_case_id_url, json=self.mocked_case_events)
        mock_request.get(self.get_available_case_group_statuses_direct_url, json=self.mocked_case_group_statuses)

        response = self.client.get(f'/case/{self.case_id}/change-response-status', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("In progress".encode(), response.data)

    @requests_mock.mock()
    def test_change_response_status(self, mock_request):
        mock_request.post(self.post_case_event)

        response = self.client.post(f'/case/{self.case_id}/change-response-status?status_updated=True&updated_'
                                    f'status=PRIVACY_DATA_CONFIDENTIALITY_CONCERNS',
                                    data={'event': 'LEGITIMACY_CONCERNS'})

        self.assertEqual(response.status_code, 302)
        self.assertIn('http://localhost/case/8849c299-5014-4637-bd2b-fc866aeccdf5?'
                      'status_updated=True&updated_status=LEGITIMACY_CONCERNS', response.location)

    @requests_mock.mock()
    def test_outcome_event_detail_is_displayed(self, mock_request):
        # Given
        with open(self.test_data_path + 'case/social_case_unknown_eligibility_status.json') as fp:
            mocked_case_details_unknown_eligibility = json.load(fp)
        with open(self.test_data_path + 'case/social_case_events_unknown_eligibility.json') as fp:
            mocked_case_events_unknown_eligibility = json.load(fp)
        mock_request.get(self.get_case_by_id_url, json=mocked_case_details_unknown_eligibility)
        mock_request.get(self.get_case_events_by_case_id_url, json=mocked_case_events_unknown_eligibility)
        mock_request.get(self.get_available_case_group_statuses_direct_url, json=self.mocked_case_group_statuses)
        mock_request.get(self.get_sample_attributes_by_id_url, json=self.mocked_sample_attributes)
        mock_request.get(self.iac_url, json=self.mocked_iacs)

        # When
        response = self.client.get(f'/case/{self.case_id}')

        # Then
        self.assertIn(b'633 Wrong Address', response.data)

    def test_group_and_order_events(self):
        # Given
        available_events = {'TOO_BUSY': '572 Too Busy',
                            'ILL_AT_HOME': '511 Ill at home during survey period: notified to Head Office',
                            'WRONG_ADDRESS': '633 Wrong Address'}
        statuses = {'EQ_LAUNCH': 'INPROGRESS',
                    'TOO_BUSY': 'OTHERNONRESPONSE',
                    'WRONG_ADDRESS': 'UNKNOWNELIGIBILITY',
                    'ILL_AT_HOME': 'OTHERNONRESPONSE'}

        expected_grouped_ordered_events = OrderedDict(
            [('500 Other Non-Response', OrderedDict(
                [('ILL_AT_HOME', '511 Ill at home during survey period: notified to Head Office'),
                 ('TOO_BUSY', '572 Too Busy')])),
             ('600 Unknown Eligibility', OrderedDict(
                 [('WRONG_ADDRESS', '633 Wrong Address')]
             ))]
        )

        # When
        actual_grouped_ordered_events = group_and_order_events(available_events, statuses)

        # Then
        self.assertEqual(expected_grouped_ordered_events, actual_grouped_ordered_events)
