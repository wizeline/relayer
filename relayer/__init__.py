from kafka import KafkaProducer

from .event_emitter import EventEmitter
from .exceptions import ConfigurationError

__version__ = '0.1.3'


class Relayer(object):

    def __init__(self, logging_topic, context_handler_class, **kwargs):
        self.logging_topic = logging_topic

        if 'kafka_hosts' not in kwargs:
            raise ConfigurationError()

        topic_prefix = kwargs.get('topic_prefix', '')
        topic_suffix = kwargs.get('topic_suffix', '')

        if 'source' not in kwargs:
            self.source = '{0}{1}{2}'.format(topic_prefix, logging_topic, topic_suffix)
        else:
            self.source = kwargs.get('source')

        self._producer = KafkaProducer(bootstrap_servers=kwargs.get('kafka_hosts'))

        self._emitter = EventEmitter(self._producer, topic_prefix=topic_prefix, topic_suffix=topic_suffix)

        self.context = context_handler_class(self._emitter)

    def emit(self, event_type, event_subtype, payload, partition_key=None):
        payload = {
            'source': self.source,
            'event_type': event_type,
            'event_subtype': event_subtype,
            'payload': payload
        }
        self.context.emit(event_type, payload, partition_key)

    def emit_raw(self, topic, message, partition_key=None):
        self.context.emit(topic, message, partition_key)

    def log(self, log_level, payload):
        message = {
            'log_level': log_level,
            'payload': payload
        }
        self.context.log(message)

    def flush(self):
        self._emitter.flush()
