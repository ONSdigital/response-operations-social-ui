import json
import os

from config import TestingConfig
from tests.views import ViewTestCase


class SocialViewTestCase(ViewTestCase):
    case_id = "8849c299-5014-4637-bd2b-fc866aeccdf5"
    sample_unit_id = "519bb700-1bd9-432d-9db7-d34ea1727415"
    collection_exercise_id = "6553d121-df61-4b3a-8f43-e0726666b8cc"
    ru_ref = "LMS0001"

    get_case_by_id_url = f'{TestingConfig.CASE_URL}/cases/{case_id}?iac=true'
    post_case_new_iac_url = f'{TestingConfig.CASE_URL}/cases/{case_id}/iac'
    iac_url = f'{TestingConfig.CASE_URL}/cases/{case_id}/iac'
    get_sample_attributes_by_id_url = f'{TestingConfig.SAMPLE_URL}/samples/{sample_unit_id}/attributes'
    get_case_events_by_case_id_url = f'{TestingConfig.CASE_URL}/cases/{case_id}/events'
    get_available_case_group_statuses_direct_url = f'{TestingConfig.CASE_URL}/casegroups/transitions' \
                                                   f'/{collection_exercise_id}/{ru_ref}'
    update_case_group_status_url = f'{TestingConfig.CASE_URL}/casegroups/transitions/{collection_exercise_id}/{ru_ref}'
    get_sample_by_id_url = f'{TestingConfig.SAMPLE_URL}/samples/{sample_unit_id}/attributes'
    get_social_mi_report = f'{TestingConfig.REPORT_URL}/reporting-api/v1/response-chasing/download-social-mi/' \
                           f'{collection_exercise_id}'

    test_data_path = os.path.join(os.path.dirname(__file__), '../../test_data/')

    with open(test_data_path + 'case/social_case.json') as fp:
        mocked_case_details = json.load(fp)
    with open(test_data_path + 'case/iacs.json') as fp:
        mocked_iacs = json.load(fp)
    with open(test_data_path + 'case/iac.json') as fp:
        mocked_iac = json.load(fp)
    with open(test_data_path + 'sample/sample_attributes.json') as fp:
        mocked_sample_attributes = json.load(fp)
    with open(test_data_path + 'case/social_case_events.json') as fp:
        mocked_case_events = json.load(fp)
    with open(test_data_path + 'case/case_group_statuses.json') as fp:
        mocked_case_group_statuses = json.load(fp)
