import logging


logger = logging.getLogger('relayer')


def log_kafka_message(topic, payload, partition_key=None):
    logger.debug('topic: %s, partition_key: %s, message: %s', topic, partition_key, payload)
