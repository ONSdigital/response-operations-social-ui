import logging
from datetime import datetime

import iso8601
import requests
from flask import current_app as app
from requests.exceptions import HTTPError
from structlog import wrap_logger

from response_operations_social_ui.exceptions.exceptions import ApiError

logger = wrap_logger(logging.getLogger(__name__))


def download_report(collection_exercise_id):
    logger.debug("Downloading response chasing report", collection_exercise_id=collection_exercise_id)

    url = (
        f"{app.config['REPORT_URL']}"
        f"/reporting-api/v1/response-chasing/download-social-mi/{collection_exercise_id}"
    )

    response = requests.get(url)

    try:
        response.raise_for_status()
    except HTTPError:
        logger.error("Error retrieving collection exercise", collection_exercise_id=collection_exercise_id)
        raise ApiError(response)

    logger.debug("Successfully downloaded response chasing report", collection_exercise_id=collection_exercise_id)
    return response


def get_collection_exercise_events(collection_exercise_id):
    logger.debug('Attempting to retrieve collection exercise events', collection_exercise_id=collection_exercise_id)
    url = f"{app.config['COLLECTION_EXERCISE_URL']}/collectionexercises/{collection_exercise_id}/events"

    response = requests.get(url, auth=app.config['COLLECTION_EXERCISE_AUTH'])

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        logger.error('Error retrieving collection exercise events', collection_exercise_id=collection_exercise_id,
                     status_code=response.status_code)
        raise ApiError(response)

    logger.debug('Successfully retrieved collection exercise events', collection_exercise_id=collection_exercise_id)
    return response.json()


def convert_events_to_new_format(events):
    formatted_events = {}
    for event in events:
        parsed_datetime = iso8601.parse_date(event['timestamp'])

        formatted_events[event['tag']] = {
            "date": parsed_datetime.strftime('%d %b %Y'),
            "month": parsed_datetime.strftime('%m'),
            "is_in_future": parsed_datetime > datetime.now(tz=parsed_datetime.tzinfo)
        }
    return formatted_events


def collection_exercise_is_closed(collection_exercise_id, tag='exercise_end'):
    events = get_collection_exercise_events(collection_exercise_id)
    return not(convert_events_to_new_format(events)[tag]['is_in_future'])
