import logging

import requests
from flask import current_app as app
from requests.exceptions import HTTPError
from structlog import wrap_logger

from response_operations_social_ui.exceptions.exceptions import ApiError

logger = wrap_logger(logging.getLogger(__name__))


def get_sample_attributes(sample_unit_id):
    logger.debug('Retrieving sample attributes from sample unit', sample_unit_id=sample_unit_id)

    url = f'{app.config["SAMPLE_URL"]}/samples/{sample_unit_id}/attributes'
    response = requests.get(url, auth=app.config['SAMPLE_AUTH'])
    try:
        response.raise_for_status()
    except HTTPError:
        logger.error('Error retrieving sample attributes', sample_unit_id=sample_unit_id,
                     status_code=response.status_code)
        raise ApiError(response)

    logger.debug('Successfully retrieved sample attributes', sample_unit_id=sample_unit_id)
    return response.json()


def search_samples_by_postcode(postcode) -> dict:
    logger.debug("Searching for samples by postcode")

    url = f'{app.config["SAMPLE_URL"]}/samples/sampleunits'
    response = requests.get(url=url,
                            auth=app.config['SAMPLE_AUTH'],
                            params={'postcode': postcode})
    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            logger.debug("No samples were found for postcode")
            return dict()
        logger.exception('Error searching for sample by postcode', status=response.status_code)
        raise ApiError(response)

    return response.json()
