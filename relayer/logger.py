from .logging import logger


def log_kafka_message(topic, payload, partition_key=None):
    if not isinstance(payload, dict):
        payload = {'message': payload}
    logger.debug('kafka_message', topic=topic, partition_key=partition_key, **payload)
