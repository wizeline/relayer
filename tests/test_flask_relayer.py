import json
from unittest import mock

import flask

from relayer.flask import FlaskRelayer

from . import BaseTestCase


class FlaskRelayerTestCase(BaseTestCase):

    @mock.patch('relayer.KafkaProducer')
    def setUp(self, kafka_producer_mock):
        self._setup_kafka_producer_mock(kafka_producer_mock)
        app = flask.Flask(__name__)
        self.app = app
        self.client = self.app.test_client()
        self.relayer = FlaskRelayer(app, 'logging_topic', 'kafka')

        @app.route('/test')
        def test_emit():
            self.relayer.emit('type', 'subtype', 'payload')
            self.relayer.log('info', 'message')
            return 'ok'

    def test_request_works_fine(self):
        self.client.get('/test').status_code.should.equal(200)

    def test_emitted_messages(self):
        self.client.get('/test')
        messages = self._get_topic_messages('type')
        messages.should.have.length_of(1)
        message = json.loads(messages[0][0].decode('utf-8'))

        message.should.have.key('event_type')
        message.should.have.key('event_subtype')
        message.should.have.key('payload')
        message['event_type'].should.equal('type')
        message['event_subtype'].should.equal('subtype')
        message['payload'].should.equal('payload')

    def test_log(self):
        self.client.get('/test')
        messages = self._get_topic_messages('logging_topic')
        messages.should.have.length_of(1)
        message = json.loads(messages[0][0].decode('utf-8'))
        message.should.have.key('date')
        message.should.have.key('user_agent')
        message.should.have.key('method')
        message.should.have.key('path')
        message.should.have.key('query_string')
        message.should.have.key('remote_addr')
        message.should.have.key('status')
        message.should.have.key('content_length')
        message.should.have.key('request_time')
        message.should.have.key('lines')
        message['lines'].should.have.length_of(2)
        first_line = message['lines'][0]
        first_line.should.have.key('event_type')
        first_line.should.have.key('event_subtype')
        first_line.should.have.key('payload')
        second_line = message['lines'][1]
        second_line.should.have.key('log_level')
        second_line.should.have.key('payload')
        second_line['log_level'].should.equal('info')
        second_line['payload'].should.equal('message')
