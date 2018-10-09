import logging

import requests
from flask import current_app as app
from requests.exceptions import HTTPError
from structlog import wrap_logger

from response_operations_social_ui.exceptions.exceptions import ApiError

logger = wrap_logger(logging.getLogger(__name__))


def download_report(collection_exercise_id):
    logger.debug(
        "Downloading response chasing report"
    )

    url = (
        f"{app.config['REPORT_URL']}"
        f"/reporting-api/v1/response-chasing/download-social-mi/{collection_exercise_id}"
    )

    response = requests.get(url)

    try:
        response.raise_for_status()
    except HTTPError:
        logger.error(
            "Error retrieving collection exercise")
        raise ApiError(response)

    logger.debug(
        "Successfully downloaded response chasing report")
    return response
