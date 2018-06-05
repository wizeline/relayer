import json

from relayer import Relayer
from relayer.rpc import make_rpc_relayer

from . import BaseTestCase


class TestRPCRelayer(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.relayer_decorator = make_rpc_relayer('logging', kafka_hosts='kafka', topic_prefix='test_', topic_suffix='_topic')
        self.logger = None

        def third_party_method() -> None:
            if self.logger:
                self.logger.log('info', 'here i am')

        @self.relayer_decorator
        def rpc_method(value: bool, relayer: Relayer) -> bool:
            relayer.emit('type', 'subtype', 'payload')
            relayer.log('info', 'message')
            return value

        @self.relayer_decorator
        def method_with_third_party(relayer: Relayer = None) -> None:
            third_party_method()

        self.rpc_method = rpc_method
        self.method_with_third_party = method_with_third_party

    def test_input_and_output_works(self) -> None:
        assert self.rpc_method(True)
        assert not self.rpc_method(False)

    def test_emitted_messages(self) -> None:
        self.rpc_method(True)
        messages = self._get_topic_messages('test_type_topic')
        assert len(messages) == 1
        message = json.loads(messages[0][0].decode('utf-8'))

        assert 'event_type' in message
        assert 'event_subtype' in message
        assert 'payload' in message
        assert message['event_type'] == 'type'
        assert message['event_subtype'] == 'subtype'
        assert message['payload'] == 'payload'

    def test_decorator_expose_instance(self) -> None:
        assert hasattr(self.relayer_decorator, 'instance')
        assert isinstance(self.relayer_decorator.instance, Relayer)  # type: ignore
