import logging

from flask_login import login_required
from structlog import wrap_logger

from response_operations_social_ui.controllers import collection_exercise_controller

logger = wrap_logger(logging.getLogger(__name__))


@login_required
def generate_social_mi_report():
    logger.debug('Generating MI report')
    response = collection_exercise_controller.download_report()
    return response.content, response.status_code, response.headers.items()
