from kafka import KafkaProducer

from .event_emitter import EventEmitter
from .exceptions import ConfigurationError

__version__ = '0.0.3'


class Relayer(object):

    def __init__(self, logging_topic, context_handler_class, kafka_hosts=None, topic_prefix='', topic_suffix=''):
        self.logging_topic = logging_topic
        if not kafka_hosts:
            raise ConfigurationError()
        producer = KafkaProducer(bootstrap_servers=kafka_hosts)
        emitter = EventEmitter(producer, topic_prefix=topic_prefix, topic_suffix=topic_suffix)
        self.context = context_handler_class(emitter)

    def emit(self, event_type, event_subtype, payload, partition_key=None):
        payload = {
            'event_type': event_type,
            'event_subtype': event_subtype,
            'payload': payload
        }
        self.context.emit(event_type, payload, partition_key)

    def log(self, log_level, payload):
        message = {
            'log_level': log_level,
            'payload': payload
        }
        self.context.log(message)
