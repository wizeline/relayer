from unittest import mock

from .mocked_producer import MockedProducer


class RelayerPatch(object):

    def __init__(self):
        self.patcher = mock.patch('relayer.KafkaProducer')

    def start(self):
        kafka_producer_mock = self.patcher.start()
        self.mocked_producer = MockedProducer()
        kafka_producer_mock.return_value = self.mocked_producer

    def stop(self):
        self.patcher.stop()
