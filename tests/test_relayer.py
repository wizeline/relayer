from relayer import Relayer
from relayer.exceptions import ConfigurationError

from . import BaseTestCase


class TestRelayer(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.relayer = Relayer('log', kafka_hosts='foo')

    def test_requires_kafka_hosts(self):
        Relayer.when.called_with('foo').should.throw(ConfigurationError)

    def test_emit(self):
        self.relayer.emit('type', 'subtype', 'payload')

    def test_emit_with_partition_key(self):
        self.relayer.emit('type', 'subtype', 'payload', 'key')

    def test_source_not_present(self):
        relayer = Relayer('log', kafka_hosts='foo', topic_prefix='pre', topic_suffix='su')
        relayer.source.should.equal('prelogsu')

    def test_source(self):
        relayer = Relayer('log', kafka_hosts='foo', source='container_1')
        relayer.source.should.equal('container_1')

    def test_emit_raw(self):
        self.relayer.emit_raw('topic', {'message': 'content'}, 'key')

    def test_flush(self):
        self.relayer.flush()
        self.relayer._producer.flushed.should.be.true
