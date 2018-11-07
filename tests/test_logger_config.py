import json
import logging
import os
import unittest

from structlog import wrap_logger

from response_operations_social_ui.logger_config import logger_initial_config


class TestLoggerConfig(unittest.TestCase):

    def test_success(self):
        os.environ['JSON_INDENT_LOGGING'] = '1'
        logger_initial_config(service_name='response-operations-social-ui')
        logger = wrap_logger(logging.getLogger())
        with self.assertLogs('', 'ERROR') as cm:
            logger.error('Test')
        message_json = json.loads(cm.records[0].message)
        message_contents = {"event": "Test", "trace": "", "span": "", "parent": "",
                            "level": "error", "service": "response-operations-social-ui"}
        for key, value in message_contents.items():
            self.assertEqual(message_json[key], value)

    def test_indent_type_error(self):
        os.environ['JSON_INDENT_LOGGING'] = 'abc'
        logger_initial_config(service_name='response-operations-social-ui')
        logger = wrap_logger(logging.getLogger())
        with self.assertLogs('', 'ERROR') as cm:
            logger.error('Test')
        message = cm.records[0].msg
        self.assertIn('"event": "Test", "trace": "", "span": "", "parent": "",'
                      ' "level": "error", "service": "response-operations-social-ui"', message)

    def test_indent_value_error(self):
        logger_initial_config(service_name='response-operations-social-ui')
        logger = wrap_logger(logging.getLogger())
        with self.assertLogs('', 'ERROR') as cm:
            logger.error('Test')
        message = cm.records[0].msg
        self.assertIn('"event": "Test", "trace": "", "span": "", "parent": "",'
                      ' "level": "error", "service": "response-operations-social-ui"', message)
