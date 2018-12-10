import logging
import os
import requestsdefaulter

import redis
from flask import Flask
from flask_assets import Bundle, Environment
from flask_login import LoginManager
from flask_session import Session
from flask_zipkin import Zipkin
from jwt.algorithms import get_default_algorithms
from structlog import wrap_logger

from response_operations_social_ui.cloud.cloudfoundry import ONSCloudFoundry
from response_operations_social_ui.logger_config import logger_initial_config
from response_operations_social_ui.maintenance import check_for_messages
from response_operations_social_ui.user import User
from response_operations_social_ui.views import setup_blueprints


def create_app(config_name=None):
    app = Flask(__name__)
    app.name = "response_operations_social_ui"

    # Load css and js assets
    assets = Environment(app)
    assets.url = app.static_url_path
    scss_min = Bundle('css/*', 'css/fonts/*', 'css/components/*',
                      filters=['cssmin'], output='minimised/all.min.css')
    assets.register('scss_all', scss_min)
    js_min = Bundle('js/*', filters='jsmin', output='minimised/all.min.js')
    assets.register('js_all', js_min)

    app_config = f'config.{config_name or os.environ.get("APP_SETTINGS", "Config")}'
    app.config.from_object(app_config)

    app.url_map.strict_slashes = False
    app.secret_key = app.config['RESPONSE_OPERATIONS_UI_SECRET']
    app.default_jwt_algorithms = get_default_algorithms().keys()

    # Zipkin
    zipkin = Zipkin(app=app, sample_rate=app.config.get("ZIPKIN_SAMPLE_RATE"))
    requestsdefaulter.default_headers(zipkin.create_http_headers_for_new_span)

    logger_initial_config(service_name='response-operations-social-ui', log_level=app.config['LOGGING_LEVEL'])
    logger = wrap_logger(logging.getLogger(__name__))
    logger.info('Logger created', log_level=app.config['LOGGING_LEVEL'])

    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = "sign_in_bp.sign_in"

    @login_manager.user_loader
    def user_loader(user_id):
        return User(user_id)

    cf = ONSCloudFoundry(redis_name=app.config['REDIS_SERVICE'])
    if cf.detected:
        with app.app_context():
            # If deploying in cloudfoundry set config to use cf redis instance
            logger.info('Cloudfoundry detected, setting service configurations')
            app.config['REDIS_HOST'] = cf.redis.credentials['host']
            app.config['REDIS_PORT'] = cf.redis.credentials['port']

    # wrap in the flask server side session manager and back it by redis
    redis_connection = redis.StrictRedis(host=app.config['REDIS_HOST'],
                                         port=app.config['REDIS_PORT'],
                                         db=app.config['REDIS_DB'])
    try:
        redis_connection.ping()
    except redis.exceptions.ConnectionError as e:
        logger.error('Failed to establish connection to redis', message=str(e))
    else:
        app.config['REDIS_CONNECTION'] = app.config['SESSION_REDIS'] = redis_connection
        Session(app)  # NB: flask-session depends on a redis connection to operate

    if app.config['DEBUG']:
        app.jinja_env.auto_reload = True

    setup_blueprints(app)

    app.before_request(check_for_messages)

    return app
