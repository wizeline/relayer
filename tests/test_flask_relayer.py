import json

import flask

from relayer.flask import FlaskRelayer

from . import BaseTestCase

TEST_KEY = 'foo_key'
TEST_VAL = 'bar_val'


class FlaskRelayerTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        app = flask.Flask(__name__)
        self.app = app
        self.client = self.app.test_client()
        self.relayer = FlaskRelayer(app, 'logging', 'kafka', topic_prefix='test_', topic_suffix='_topic')

        @app.route('/test')
        def test_emit() -> str:
            self.relayer.emit('type', 'subtype', 'payload')
            self.relayer.log('info', 'message')
            return 'ok'

        @app.route('/test_raw')
        def test_emit_raw() -> str:
            self.relayer.emit_raw('raw', {TEST_KEY: TEST_VAL})
            return 'ok'

        @app.route('/test_flush')
        def test_log_and_flush() -> str:
            self.relayer.log('info', 'message')
            self.relayer.flush()
            return 'ok'

    def test_request_works_fine(self) -> None:
        assert self.client.get('/test').status_code == 200

    def test_emitted_messages(self) -> None:
        self.client.get('/test')
        messages = self._get_topic_messages('test_type_topic')
        assert len(messages) == 1
        message = json.loads(messages[0][0].decode('utf-8'))

        assert 'event_type' in message
        assert message['event_type'] == 'type'
        assert 'event_subtype' in message
        assert message['event_subtype'] == 'subtype'
        assert 'payload' in message
        assert message['payload'] == 'payload'

    def test_emitted_raw_messages(self) -> None:
        self.client.get('/test_raw')
        messages = self._get_topic_messages('test_raw_topic')
        assert len(messages) == 1
        message = json.loads(messages[0][0].decode('utf-8'))
        assert TEST_KEY in message
        assert message[TEST_KEY] == TEST_VAL

    def test_flush(self) -> None:
        self.client.get('/test_flush')
        assert self.producer.flushed
