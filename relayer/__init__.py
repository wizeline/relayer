from kafka import KafkaProducer

from .event_emitter import EventEmitter
from .exceptions import ConfigurationError

__version__ = '0.2.0'


class Relayer(object):
    """
    Arguments:
        logging_topic: desired kafka topic to send logs, this will get modified if a prefix o suffix is set.
        context_handler_class: class that receives an emitter and expose at least a method emit and log.
    Keyword Arguments:
        kafka_hosts: 'host[:port]' string (or list of 'host[:port]'
            strings) that the producer should contact to bootstrap initial
            cluster metadata. This does not have to be the full node list.
            It just needs to have at least one broker that will respond to a
            Metadata API Request.
        topic_prefix: value to prefix all topics handled by relayer.
            Defaults to empty string.
        topic_suffix: value to suffix all topics handled by relayer.
            Defaults to empty string.
        source: This value will be added as a top level key in your payloads
            when using emit or log. If defined it must be a json serializable
            value. Defaults to topic_prefix + logging_topic + topic_suffix.
        producer_opts: optional dictionary with the configuration
            for http://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
    """

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

        producer_opts = kwargs.get('producer_opts', {})
        self._producer = KafkaProducer(bootstrap_servers=kwargs.get('kafka_hosts'), **producer_opts)

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
