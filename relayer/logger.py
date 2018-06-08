from typing import Dict, Any, Union
from .logging import logger


def log_kafka_message(topic: str, payload: Union[Dict[Any, Any], str], partition_key: str = None) -> None:
    if not isinstance(payload, dict):
        payload = {'message': payload}
    logger.debug('kafka_message', topic=topic, partition_key=partition_key, **payload)
