import logging

import jwt
from flask import current_app
from structlog import wrap_logger

from response_operations_social_ui.common.uaa import get_uaa_public_key


logger = wrap_logger(logging.getLogger(__name__))


def decode_access_token(access_token):
    return jwt.decode(
        access_token,
        key=get_uaa_public_key(),
        audience='response_operations_social',
        leeway=10,
        algorithms=current_app.default_jwt_algorithms,
    )
