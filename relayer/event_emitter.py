import json
from uuid import UUID

from .exceptions import NonJSONSerializableMessageError, UnsupportedPartitionKeyTypeError


class EventEmitter(object):

    def __init__(self, producer):
        self.producer = producer

    def emit(self, topic, message, partition_key=None):

        if isinstance(partition_key, str):
            partition_key = partition_key.encode('utf-8')
        elif isinstance(partition_key, UUID):
            partition_key = partition_key.bytes
        elif partition_key is not None:
            raise UnsupportedPartitionKeyTypeError(partition_key.__class__)

        try:
            message = json.dumps(message).encode('utf-8')
        except TypeError as error:
            raise NonJSONSerializableMessageError(str(error))

        self.producer.send(topic, key=partition_key, value=message)

    def flush(self):
        self.producer.flush()
