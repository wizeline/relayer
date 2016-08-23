import json

import flask

from relayer.flask import FlaskRelayer

from . import BaseTestCase


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

    def test_request_works_fine(self):
        self.client.get('/test').status_code.should.equal(200)

    def test_emitted_messages(self):
        self.client.get('/test')
        messages = self._get_topic_messages('test_type_topic')
        messages.should.have.length_of(1)
        message = json.loads(messages[0][0].decode('utf-8'))

        message.should.have.key('event_type')
        message.should.have.key('event_subtype')
        message.should.have.key('payload')
        message['event_type'].should.equal('type')
        message['event_subtype'].should.equal('subtype')
        message['payload'].should.equal('payload')

    def test_x_forwarded_for(self):
        real_ip = '127.0.0.1'
        ips = '127.0.0.1,192.168.99.100'
        self.client.get('/test', headers={'X-Forwarded-For': ips, 'X-Real-IP': '127.0.0.1'})
        messages = self._get_topic_messages('test_logging_topic')
        messages.should.have.length_of(1)
        message = json.loads(messages[0][0].decode('utf-8'))

        message.should.have.key('x_forwarded_for').should.equal(ips)
        message.should.have.key('remote_addr').should.equal(real_ip)

    def test_log(self):
        self.client.get('/test')
        messages = self._get_topic_messages('test_logging_topic')
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
