import unittest

from response_operations_social_ui.common.social_outcomes import SOCIAL_OUTCOMES_MAP
from response_operations_social_ui.views.social.social_case_context import get_case_event_description


class TestSocialCaseContext(unittest.TestCase):

    def test_get_case_event_description(self):
        case_events = [
            {
                'createdDateTime': '2018-01-01T00:00:00.000Z',
                'category': 'PRIVACY_DATA_CONFIDENTIALITY_CONCERNS'
            }
        ]

        event_description = get_case_event_description('REFUSAL', case_events)
        self.assertEqual(event_description,
                         SOCIAL_OUTCOMES_MAP.get('PRIVACY_DATA_CONFIDENTIALITY_CONCERNS').formatted_string)

    def test_get_case_event_description_event_does_not_exist(self):
        case_events = [
            {
                'createdDateTime': '2018-01-01T00:00:00.000Z',
                'category': 'NO_MATCHING_EVENTS_HERE'
            }
        ]

        event_description = get_case_event_description('REFUSAL', case_events)
        self.assertIsNone(event_description)
