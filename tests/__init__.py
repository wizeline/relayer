import sure  # noqa
from unittest import TestCase

from relayer.test import RelayerPatch


class BaseTestCase(TestCase):

    def setUp(self):
        self.relayer_patch = RelayerPatch()
        self.relayer_patch.start()
        self.producer = self.relayer_patch.mocked_producer

    def tearDown(self):
        if hasattr(self, 'relayer_patch'):
            self.relayer_patch.stop()

    def _get_topic_messages(self, topic):
        return self.producer.produced_messages[topic]
