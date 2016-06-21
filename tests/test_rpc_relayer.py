import json
from unittest import mock

from relayer.rpc import make_rpc_relayer

from . import BaseTestCase


class TestRPCRelayer(BaseTestCase):

    @mock.patch('relayer.KafkaProducer')
    def setUp(self, kafka_producer_mock):
        self._setup_kafka_producer_mock(kafka_producer_mock)

        relayer = make_rpc_relayer('logging_topic', kafka_hosts='kafka')

        @relayer
        def rpc_method(value, relayer=None):
            relayer.emit('type', 'subtype', 'payload')
            relayer.log('info', 'message')
            return value

        self.rpc_method = rpc_method

    def test_input_and_output_works(self):
        self.rpc_method(True).should.be.true
        self.rpc_method(False).should.be.false

    def test_emitted_messages(self):
        self.rpc_method(True)
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
        self.rpc_method(True)
        messages = self._get_topic_messages('logging_topic')
        messages.should.have.length_of(1)
        message = json.loads(messages[0][0].decode('utf-8'))
        message.should.have.key('date')
        message.should.have.key('service')
        message.should.have.key('service_time')
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
