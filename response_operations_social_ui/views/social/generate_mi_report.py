import logging

from flask_login import login_required
from structlog import wrap_logger

from response_operations_social_ui.controllers import collection_exercise_controller

logger = wrap_logger(logging.getLogger(__name__))


@login_required
def generate_social_mi_report(collection_exercise_id):
    logger.debug('Generating social MI report', collection_exercise_id=collection_exercise_id)
    response = collection_exercise_controller.download_report(collection_exercise_id)
    return response.content, response.status_code, response.headers.items()
