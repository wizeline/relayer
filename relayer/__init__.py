from typing import Any, Dict, Union
from kafka import KafkaProducer

from .event_emitter import EventEmitter
from .exceptions import ConfigurationError
from .logging import logger as log

__version__ = '2.0.4'


class Relayer(object):
    """
    Arguments:
        logging_topic: desired kafka topic to send logs, this will get modified if a prefix o suffix is set.
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

    def __init__(self, logging_topic: str, **kwargs: str) -> None:
        self.logging_topic = logging_topic

        if 'kafka_hosts' not in kwargs:
            raise ConfigurationError()

        topic_prefix = kwargs.get('topic_prefix', '')
        topic_suffix = kwargs.get('topic_suffix', '')

        self.source = kwargs.get('source', '{0}{1}{2}'.format(topic_prefix, logging_topic, topic_suffix))

        producer_opts = kwargs.get('producer_opts', {})
        self._producer = KafkaProducer(bootstrap_servers=kwargs.get('kafka_hosts'), **producer_opts)

        self._emitter = EventEmitter(self._producer, topic_prefix=topic_prefix, topic_suffix=topic_suffix)

    def emit(self, event_type: str, event_subtype: str, payload: Union[Dict[Any, Any], str], partition_key: str = None) -> None:
        message = {
            'source': self.source,
            'event_type': event_type,
            'event_subtype': event_subtype,
            'payload': payload
        }
        self._emitter.emit(event_type, message, partition_key)

    def emit_raw(self, topic: str, message: Dict[Any, Any], partition_key: str = None) -> None:
        self._emitter.emit(topic, message, partition_key)

    def log(self, log_level: str, payload: Union[Dict[Any, Any], str]) -> None:
        if not isinstance(payload, dict):
            log_payload = {'message': payload}
        else:
            log_payload = payload

        log.debug('relayer_logger_deprecated')
        log.info('relayer_log', log_level=log_level, **log_payload)  # logger.log isn't working properly

    def flush(self) -> None:
        self._emitter.flush()
