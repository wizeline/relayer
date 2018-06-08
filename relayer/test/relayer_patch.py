from unittest import mock

from .mocked_producer import MockedProducer


class RelayerPatch(object):

    def __init__(self) -> None:
        self.patcher = mock.patch('relayer.KafkaProducer')

    def start(self) -> None:
        kafka_producer_mock = self.patcher.start()
        self.mocked_producer = MockedProducer()
        kafka_producer_mock.return_value = self.mocked_producer

    def stop(self) -> None:
        self.patcher.stop()
