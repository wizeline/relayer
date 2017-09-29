from relayer import Relayer


class FlaskRelayer(object):

    def __init__(self, app=None, logging_topic=None, kafka_hosts=None, **kwargs):
        if app:
            self.init_app(
                app,
                logging_topic,
                kafka_hosts=kafka_hosts,
                **kwargs,
            )

    def init_app(self, app, logging_topic, kafka_hosts=None, **kwargs):
        kafka_hosts = kafka_hosts or app.config.get('KAFKA_HOSTS')
        self.event_relayer = Relayer(
            logging_topic,
            kafka_hosts=kafka_hosts,
            **kwargs,
        )

    def emit(self, *args, **kwargs):
        self.event_relayer.emit(*args, **kwargs)

    def emit_raw(self, *args, **kwargs):
        self.event_relayer.emit_raw(*args, **kwargs)

    def log(self, *args, **kwargs):
        self.event_relayer.log(*args, **kwargs)

    def flush(self, *args, **kwargs):
        self.event_relayer.flush(*args, **kwargs)
