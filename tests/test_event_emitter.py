from uuid import uuid4
from datetime import datetime
import json

from relayer import EventEmitter
from relayer.test import MockedProducer
from relayer.exceptions import NonJSONSerializableMessageError, UnsupportedPartitionKeyTypeError

from . import BaseTestCase


class TestEventEmitter(BaseTestCase):
    def setUp(self) -> None:
        self.producer = MockedProducer()
        self.emitter = EventEmitter(self.producer)

    def test_sending_message(self) -> None:
        self.emitter.emit('foo', {'foo_key': 'bar_val'})
        messages = self._get_topic_messages('foo')
        assert len(messages) == 1
        message = json.loads(messages[0][0].decode('utf-8'))
        assert 'foo_key' in message
        assert message['foo_key'] == 'bar_val'

    def test_throws_if_not_sending_json_serializable(self) -> None:
        self.assertRaises(NonJSONSerializableMessageError, self.emitter.emit, 'foo', datetime.utcnow())

    def test_incorrect_partition_key(self) -> None:
        self.assertRaises(UnsupportedPartitionKeyTypeError, self.emitter.emit, 'foo', 'bar', datetime.utcnow())
        # self.emitter.emit.when.called_with('foo', 'bar', datetime.utcnow()).should.throw(UnsupportedPartitionKeyTypeError)

    def test_string_partition_key(self) -> None:
        self.emitter.emit('foo', {'foo': 'bar'}, partition_key='key')
        messages = self._get_topic_messages('foo')
        assert len(messages) == 1
        assert b'key' in messages[0][1]

    def test_uuid_partition_key(self) -> None:
        key = uuid4()
        self.emitter.emit('foo', {'foo': 'bar'}, partition_key=key)
        messages = self._get_topic_messages('foo')
        assert len(messages) == 1
        assert key.bytes in messages[0][1]

    def test_flush(self) -> None:
        self.emitter.flush()
        assert self.producer.flushed

    def test_message_prefix(self) -> None:
        self.emitter = EventEmitter(self.producer, topic_prefix='test_')
        self.emitter.emit('foo', {'foo': 'bar'})
        assert len(self._get_topic_messages('test_foo')) == 1

    def test_message_suffix(self) -> None:
        self.emitter = EventEmitter(self.producer, topic_suffix='_test')
        self.emitter.emit('foo', {'foo': 'bar'})
        assert len(self._get_topic_messages('foo_test')) == 1
