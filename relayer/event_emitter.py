from typing import Any, Dict
from datetime import datetime
from uuid import UUID
import json

from kafka import KafkaProducer

from .exceptions import NonJSONSerializableMessageError, UnsupportedPartitionKeyTypeError
from .logger import log_kafka_message


class EventEmitter(object):

    def __init__(self, producer: KafkaProducer, topic_prefix: str = '', topic_suffix: str = '') -> None:
        self.producer = producer
        self.topic_prefix = topic_prefix
        self.topic_suffix = topic_suffix

    def emit(self, topic: str, message: Dict[Any, Any], partition_key: Any = None) -> None:

        topic = '{0}{1}{2}'.format(self.topic_prefix, topic, self.topic_suffix)

        log_kafka_message(topic, message, partition_key=partition_key)

        if isinstance(partition_key, str):
            partition_key = partition_key.encode('utf-8')
        elif isinstance(partition_key, UUID):
            partition_key = partition_key.bytes
        elif partition_key is not None:
            raise UnsupportedPartitionKeyTypeError(partition_key.__class__)

        try:
            message.update({'timestamp': '{0}Z'.format(datetime.utcnow().isoformat())})
            msg = json.dumps(message).encode('utf-8')
        except (TypeError, AttributeError) as error:
            raise NonJSONSerializableMessageError(str(error))

        self.producer.send(topic, key=partition_key, value=msg)

    def flush(self) -> None:
        self.producer.flush()
