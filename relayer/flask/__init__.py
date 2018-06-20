from typing import Any

from flask import Flask
from relayer import Relayer


class FlaskRelayer(object):

    def __init__(self, app: Flask = None, logging_topic: str = None, kafka_hosts: str = None, **kwargs: str) -> None:
        if app:
            self.init_app(
                app,
                logging_topic,
                kafka_hosts=kafka_hosts,
                **kwargs,
            )

    def init_app(self, app: Flask, logging_topic: Any, kafka_hosts: str = None, **kwargs: str) -> None:
        kafka_hosts = kafka_hosts or app.config.get('KAFKA_HOSTS')
        self.event_relayer = Relayer(
            logging_topic,
            kafka_hosts=kafka_hosts,
            **kwargs,
        )

    def emit(self, *args: str, **kwargs: str) -> None:
        self.event_relayer.emit(*args, **kwargs)

    def emit_raw(self, *args: Any, **kwargs: Any) -> None:
        self.event_relayer.emit_raw(*args, **kwargs)

    def log(self, *args: str, **kwargs: str) -> None:
        self.event_relayer.log(*args, **kwargs)

    def flush(self, *args: str, **kwargs: str) -> None:
        self.event_relayer.flush()
