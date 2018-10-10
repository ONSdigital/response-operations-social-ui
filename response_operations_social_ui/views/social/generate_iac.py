import logging

from flask import request, flash, redirect, url_for
from flask_login import login_required
from structlog import wrap_logger

from response_operations_social_ui.controllers import case_controller

logger = wrap_logger(logging.getLogger(__name__))


@login_required
def generate_iac():
    case_id = request.form['case_id']
    logger.debug("Generating new IAC for case", case_id=case_id)
    new_iac = case_controller.generate_iac(case_id)

    flash(new_iac, 'new_iac')
    return redirect(url_for('social_bp.view_social_case_details', case_id=case_id))
