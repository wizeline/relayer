import json

from relayer import Relayer
from relayer.rpc import make_rpc_relayer

from . import BaseTestCase


class TestRPCRelayer(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.relayer_decorator = make_rpc_relayer('logging', kafka_hosts='kafka', topic_prefix='test_', topic_suffix='_topic')
        self.logger = None

        def third_party_method():
            if self.logger:
                self.logger.log('info', 'here i am')

        @self.relayer_decorator
        def rpc_method(value, relayer=None):
            relayer.emit('type', 'subtype', 'payload')
            relayer.log('info', 'message')
            return value

        @self.relayer_decorator
        def method_with_third_party(relayer=None):
            third_party_method()

        self.rpc_method = rpc_method
        self.method_with_third_party = method_with_third_party

    def test_input_and_output_works(self):
        self.rpc_method(True).should.be.true
        self.rpc_method(False).should.be.false

    def test_emitted_messages(self):
        self.rpc_method(True)
        messages = self._get_topic_messages('test_type_topic')
        messages.should.have.length_of(1)
        message = json.loads(messages[0][0].decode('utf-8'))

        message.should.have.key('event_type')
        message.should.have.key('event_subtype')
        message.should.have.key('payload')
        message['event_type'].should.equal('type')
        message['event_subtype'].should.equal('subtype')
        message['payload'].should.equal('payload')

    def test_decorator_expose_instance(self):
        self.relayer_decorator.should.have.property('instance')
        self.relayer_decorator.instance.should.be.a(Relayer)
