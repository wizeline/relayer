from relayer import Relayer
from relayer.exceptions import ConfigurationError

from . import BaseTestCase
from .mocks import MockedContextHandler


class TestRelayer(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.relayer = Relayer('log', MockedContextHandler, kafka_hosts='foo')

    def test_requires_kafka_hosts(self):
        Relayer.when.called_with('foo', MockedContextHandler).should.throw(ConfigurationError)

    def test_emit(self):
        self.relayer.emit('type', 'subtype', 'payload')
        self.relayer.context.topic.should.equal('type')

    def test_emit_with_partition_key(self):
        self.relayer.emit('type', 'subtype', 'payload', 'key')
        self.relayer.context.partition_key.should.equal('key')
        context_message = self.relayer.context.message
        context_message.should.have.key('source').which.should.equal(self.relayer.source)
        context_message.should.have.key('event_type').which.should.equal('type')
        context_message.should.have.key('event_subtype').which.should.equal('subtype')
        context_message.should.have.key('payload').which.should.equal('payload')

    def test_log(self):
        self.relayer.log('info', 'message')
        log_message = self.relayer.context.log_message
        log_message.should.have.key('log_level')
        log_message.should.have.key('payload')
        log_message['log_level'].should.equal('info')
        log_message['payload'].should.equal('message')

    def test_source_not_present(self):
        relayer = Relayer('log', MockedContextHandler, kafka_hosts='foo', topic_prefix='pre', topic_suffix='su')
        relayer.source.should.equal('prelogsu')

    def test_source(self):
        relayer = Relayer('log', MockedContextHandler, kafka_hosts='foo', source='container_1')
        relayer.source.should.equal('container_1')
