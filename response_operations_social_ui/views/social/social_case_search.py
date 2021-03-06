import logging

from flask import render_template, request
from flask_login import login_required
from structlog import wrap_logger

from response_operations_social_ui.controllers.case_controller import get_cases_by_sample_unit_id
from response_operations_social_ui.controllers.sample_controllers import search_samples_by_postcode


logger = wrap_logger(logging.getLogger(__name__))


@login_required
def social_case_search():
    postcode = request.args.get('query')

    if postcode:
        results = get_cases_by_postcode(postcode)
        return render_template('social.html',
                               results=results,
                               postcode=postcode)

    return render_template('social.html',
                           results=None)


def get_cases_by_postcode(postcode):
    sample_units = search_samples_by_postcode(postcode)

    if not sample_units:
        return {}

    sample_unit_ids = [sample_unit['id'] for sample_unit in sample_units]

    cases = get_cases_by_sample_unit_id(sample_unit_ids)

    case_attributes = []
    for case in cases:
        for sample_unit in sample_units:
            if sample_unit['id'] == case['sampleUnitId']:
                case_attributes.append({
                    'case': case,
                    'attributes': sample_unit['sampleAttributes']['attributes'],
                    'address': format_address_for_results(sample_unit['sampleAttributes']['attributes'])
                })

    return case_attributes


def format_address_for_results(sample_unit_attributes):
    return ', '.join(filter(None, (sample_unit_attributes.get('ADDRESS_LINE1'),
                                   sample_unit_attributes.get('ADDRESS_LINE2'),
                                   sample_unit_attributes.get('LOCALITY'),
                                   sample_unit_attributes.get('TOWN_NAME'))))
