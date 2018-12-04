import json
import logging

import redis
from flask import current_app, g
from structlog import wrap_logger


logger = wrap_logger(logging.getLogger(__name__))


def check_for_messages():  # pylint: disable=unused-variable
    try:
        redis_connection = current_app.config['REDIS_CONNECTION']
        maintenance_message = redis_connection.get(current_app.config['REDIS_MAINTENANCE_KEY'])
        if maintenance_message:
            maintenance_message = json.loads(maintenance_message)
            logger.info('Maintenance message received from redis')
            g.maintenance_message = maintenance_message
    except KeyError:
        logger.debug('Redis connection does not exist')
    except redis.exceptions.RedisError as e:
        logger.error('Failed to connect to redis', message=str(e))
    except TypeError as e:
        logger.error('Unexpected message type received from redis', message=str(e))
