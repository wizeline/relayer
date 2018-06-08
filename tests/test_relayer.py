from relayer import Relayer
from relayer.exceptions import ConfigurationError

from . import BaseTestCase


class TestRelayer(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.relayer = Relayer('log', kafka_hosts='foo')

    def test_requires_kafka_hosts(self) -> None:
        self.assertRaises(ConfigurationError, Relayer, 'foo')

    def test_emit(self) -> None:
        self.relayer.emit('type', 'subtype', 'payload')

    def test_emit_with_partition_key(self) -> None:
        self.relayer.emit('type', 'subtype', 'payload', 'key')

    def test_source_not_present(self) -> None:
        relayer = Relayer('log', kafka_hosts='foo', topic_prefix='pre', topic_suffix='su')
        assert relayer.source == 'prelogsu'

    def test_source(self) -> None:
        relayer = Relayer('log', kafka_hosts='foo', source='container_1')
        assert relayer.source == 'container_1'

    def test_emit_raw(self) -> None:
        self.relayer.emit_raw('topic', {'message': 'content'}, 'key')

    def test_flush(self) -> None:
        self.relayer.flush()
        assert self.relayer._producer.flushed
