import json

import flask

from relayer.flask import FlaskRelayer

from . import BaseTestCase

TEST_KEY = 'foo_key'
TEST_VAL = 'bar_val'


class FlaskRelayerTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        app = flask.Flask(__name__)
        self.app = app
        self.client = self.app.test_client()
        self.relayer = FlaskRelayer(app, 'logging', 'kafka', topic_prefix='test_', topic_suffix='_topic')

        @app.route('/test')
        def test_emit():
            self.relayer.emit('type', 'subtype', 'payload')
            self.relayer.log('info', 'message')
            return 'ok'

        @app.route('/test_raw')
        def test_emit_raw():
            self.relayer.emit_raw('raw', {TEST_KEY: TEST_VAL})
            return 'ok'

        @app.route('/test_flush')
        def test_log_and_flush():
            self.relayer.log('info', 'message')
            self.relayer.flush()
            return 'ok'

    def test_request_works_fine(self):
        self.client.get('/test').status_code.should.equal(200)

    def test_emitted_messages(self):
        self.client.get('/test')
        messages = self._get_topic_messages('test_type_topic')
        messages.should.have.length_of(1)
        message = json.loads(messages[0][0].decode('utf-8'))

        message.should.have.key('event_type').being.equal('type')
        message.should.have.key('event_subtype').being.equal('subtype')
        message.should.have.key('payload').being.equal('payload')

    def test_emitted_raw_messages(self):
        self.client.get('/test_raw')
        messages = self._get_topic_messages('test_raw_topic')
        messages.should.have.length_of(1)
        message = json.loads(messages[0][0].decode('utf-8'))
        message.should.contain(TEST_KEY)
        message[TEST_KEY].should.equal(TEST_VAL)

    def test_flush(self):
        self.client.get('/test_flush')
        self.producer.flushed.should.be.true
