from relayer import Relayer
from .flask_context_handler import FlaskContextHandler
from .logging_middleware import LoggingMiddleware


class FlaskRelayer(object):

    def __init__(self, app=None, logging_topic=None, kafka_hosts=None, topic_prefix='', topic_suffix=''):
        if app:
            self.init_app(app, logging_topic, kafka_hosts=kafka_hosts, topic_prefix=topic_prefix,
                          topic_suffix=topic_suffix)

    def init_app(self, app, logging_topic, kafka_hosts=None, topic_prefix='', topic_suffix=''):
        kafka_hosts = kafka_hosts or app.config.get('KAFKA_HOSTS')
        self.event_relayer = Relayer(logging_topic, FlaskContextHandler, kafka_hosts=kafka_hosts, topic_prefix=topic_prefix,
                                     topic_suffix=topic_suffix)
        app.wsgi_app = LoggingMiddleware(app, app.wsgi_app, self.event_relayer.context, logging_topic)

    def emit(self, *args, **kwargs):
        self.event_relayer.emit(*args, **kwargs)

    def log(self, *args, **kwargs):
        self.event_relayer.log(*args, **kwargs)
