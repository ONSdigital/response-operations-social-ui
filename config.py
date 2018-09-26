import os
from distutils.util import strtobool

FDI_LIST = {'AOFDI', 'AIFDI', 'QIFDI', 'QOFDI'}


class Config(object):

    DEBUG = os.getenv('DEBUG', False)
    TESTING = False
    PORT = os.getenv('PORT', 8086)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
    RESPONSE_OPERATIONS_UI_SECRET = os.getenv('RESPONSE_OPERATIONS_UI_SECRET', "secret")
    SESSION_TYPE = "redis"
    PERMANENT_SESSION_LIFETIME = os.getenv('PERMANENT_SESSION_LIFETIME', 43200)
    REDIS_SERVICE = os.getenv('REDIS_SERVICE')
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_DB = os.getenv('REDIS_DB', 0)
    SECURE_COOKIES = strtobool(os.getenv('SECURE_COOKIES', 'True'))
    USE_SESSION_FOR_NEXT = True

    # Zipkin
    ZIPKIN_DISABLE = bool(strtobool(os.getenv("ZIPKIN_DISABLE", "False")))
    ZIPKIN_DSN = os.getenv("ZIPKIN_DSN", None)
    ZIPKIN_SAMPLE_RATE = int(os.getenv("ZIPKIN_SAMPLE_RATE", 0))

    # Service Configs
    CASE_URL = os.getenv('CASE_URL')
    CASE_USERNAME = os.getenv('CASE_USERNAME')
    CASE_PASSWORD = os.getenv('CASE_PASSWORD')
    CASE_AUTH = (CASE_USERNAME, CASE_PASSWORD)

    IAC_URL = os.getenv('IAC_URL')
    IAC_USERNAME = os.getenv('IAC_USERNAME')
    IAC_PASSWORD = os.getenv('IAC_PASSWORD')
    IAC_AUTH = (IAC_USERNAME, IAC_PASSWORD)

    SAMPLE_URL = os.getenv('SAMPLE_URL')
    SAMPLE_USERNAME = os.getenv('SAMPLE_USERNAME')
    SAMPLE_PASSWORD = os.getenv('SAMPLE_PASSWORD')
    SAMPLE_AUTH = (SAMPLE_USERNAME, SAMPLE_PASSWORD)

    UAA_SERVICE_URL = os.getenv('UAA_SERVICE_URL')
    UAA_CLIENT_ID = os.getenv('UAA_CLIENT_ID')
    UAA_CLIENT_SECRET = os.getenv('UAA_CLIENT_SECRET')


class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG', True)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
    REDIS_HOST = os.getenv('REDIS_HOST', "localhost")
    REDIS_PORT = os.getenv('REDIS_PORT', 7379)
    REDIS_DB = os.getenv('REDIS_DB', 0)
    SECURE_COOKIES = strtobool(os.getenv('SECURE_COOKIES', 'False'))

    # Service Config
    CASE_URL = os.getenv('CASE_URL', 'http://localhost:8171')
    CASE_USERNAME = os.getenv('CASE_USERNAME', 'admin')
    CASE_PASSWORD = os.getenv('CASE_PASSWORD', 'secret')
    CASE_AUTH = (CASE_USERNAME, CASE_PASSWORD)

    IAC_URL = os.getenv('IAC_URL', 'http://localhost:8121')
    IAC_USERNAME = os.getenv('IAC_USERNAME', 'admin')
    IAC_PASSWORD = os.getenv('IAC_PASSWORD', 'secret')
    IAC_AUTH = (IAC_USERNAME, IAC_PASSWORD)

    SAMPLE_URL = os.getenv('SAMPLE_URL', 'http://localhost:8125')
    SAMPLE_USERNAME = os.getenv('SAMPLE_USERNAME', 'admin')
    SAMPLE_PASSWORD = os.getenv('SAMPLE_PASSWORD', 'secret')
    SAMPLE_AUTH = (SAMPLE_USERNAME, SAMPLE_PASSWORD)

    UAA_SERVICE_URL = os.getenv('UAA_SERVICE_URL', 'http://localhost:9080')
    UAA_CLIENT_ID = os.getenv('UAA_CLIENT_ID', 'response_operations_social')
    UAA_CLIENT_SECRET = os.getenv('UAA_CLIENT_SECRET', 'password')


class TestingConfig(DevelopmentConfig):
    DEBUG = False
    TESTING = True
    LOGIN_DISABLED = True
    WTF_CSRF_ENABLED = False
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    UAA_PUBLIC_KEY = 'Test'
    SECRET_KEY = 'sekrit!'

