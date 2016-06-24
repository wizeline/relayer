from uuid import uuid4
from datetime import datetime

from relayer import EventEmitter
from relayer.test import MockedProducer
from relayer.exceptions import NonJSONSerializableMessageError, UnsupportedPartitionKeyTypeError

from . import BaseTestCase


class TestEventEmitter(BaseTestCase):

    def setUp(self):
        self.producer = MockedProducer()
        self.emitter = EventEmitter(self.producer)

    def test_sending_message(self):
        self.emitter.emit('foo', 'bar')
        messages = self._get_topic_messages('foo')
        messages.should.have.length_of(1)
        messages[0][0].should.equal(b'"bar"')

    def test_throws_if_not_sending_json_serializable(self):
        self.emitter.emit.when.called_with('foo', datetime.utcnow()).should.throw(NonJSONSerializableMessageError)

    def test_incorrect_partition_key(self):
        self.emitter.emit.when.called_with('foo', 'bar', datetime.utcnow()).should.throw(UnsupportedPartitionKeyTypeError)

    def test_string_partition_key(self):
        self.emitter.emit('foo', 'bar', partition_key='key')
        messages = self._get_topic_messages('foo')
        messages.should.have.length_of(1)
        messages[0][1].should.equal(b'key')

    def test_uuid_partition_key(self):
        key = uuid4()
        self.emitter.emit('foo', 'bar', partition_key=key)
        messages = self._get_topic_messages('foo')
        messages.should.have.length_of(1)
        messages[0][1].should.equal(key.bytes)

    def test_flush(self):
        self.emitter.flush()
        self.producer.flushed.should.be.true

    def test_message_prefix(self):
        self.emitter = EventEmitter(self.producer, topic_prefix='test_')
        self.emitter.emit('foo', 'bar')
        self._get_topic_messages('test_foo').should.have.length_of(1)

    def test_message_suffix(self):
        self.emitter = EventEmitter(self.producer, topic_suffix='_test')
        self.emitter.emit('foo', 'bar')
        self._get_topic_messages('foo_test').should.have.length_of(1)
