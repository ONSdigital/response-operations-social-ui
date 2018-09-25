from response_operations_social_ui.views.errors import error_bp
from response_operations_social_ui.views.info import info_bp
from response_operations_social_ui.views.logout import logout_bp
from response_operations_social_ui.views.sign_in import sign_in_bp
from response_operations_social_ui.views.social import social_bp


def setup_blueprints(app):
    app.register_blueprint(error_bp, url_prefix='/errors')
    app.register_blueprint(info_bp, url_prefix='/info')
    app.register_blueprint(logout_bp, url_prefix='/logout')
    app.register_blueprint(sign_in_bp, url_prefix='/sign-in')
    app.register_blueprint(social_bp, url_prefix='/')
    return app
