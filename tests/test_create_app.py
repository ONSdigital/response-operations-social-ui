import json
import os
import unittest

from flask import app

from response_operations_social_ui import create_app


class TestCreateApp(unittest.TestCase):

    vcap_services = {
        'broker-name': [
            {
                'credentials': {
                    'host': 'test_host',
                    'name': 'redis-hostname',
                    'port': 'test_port'
                },
                'label': 'broker-name',
                'name': 'test-redis',
                'plan': 'small',
                'provider': None,
                'syslog_drain_url': None,
                'tags': ['redis'],
                'volume_mounts': []
            }
        ]
    }

    def tearDown(self):
        try:
            del os.environ['VCAP_SERVICES']
            del os.environ['VCAP_APPLICATION']
        except KeyError:
            pass

    def setUp(self):
        app.testing = True
        os.environ['APP_SETTINGS'] = 'TestingConfig'

    # Check that we can initialise app and access it's config
    def test_create_app(self):
        test_app = create_app('TestingConfig')
        self.assertEqual(test_app.config['REDIS_HOST'], 'localhost')

    def test_create_app_with_cf(self):
        os.environ['VCAP_APPLICATION'] = json.dumps(True)
        os.environ['VCAP_SERVICES'] = json.dumps(self.vcap_services)

        test_app = create_app()
        self.assertEqual(test_app.config['REDIS_HOST'], 'test_host')
        self.assertEqual(test_app.config['REDIS_PORT'], 'test_port')
