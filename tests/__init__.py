import sure  # noqa
from unittest import TestCase

from .mocks import MockedProducer


class BaseTestCase(TestCase):
    def _setup_kafka_producer_mock(self, kafka_producer_mock):
        mock_instance = MockedProducer()
        kafka_producer_mock.return_value = mock_instance
        self.producer = mock_instance

    def _get_topic_messages(self, topic):
        return self.producer.produced_messages[topic]
