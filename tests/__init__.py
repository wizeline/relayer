from typing import List, Any
import sure  # noqa
from unittest import TestCase

from relayer.test import RelayerPatch


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.relayer_patch = RelayerPatch()
        self.relayer_patch.start()
        self.producer = self.relayer_patch.mocked_producer

    def tearDown(self) -> None:
        if hasattr(self, 'relayer_patch'):
            self.relayer_patch.stop()

    def _get_topic_messages(self, topic: str) -> List[Any]:
        return self.producer.produced_messages[topic]
