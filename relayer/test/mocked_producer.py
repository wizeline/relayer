from collections import defaultdict


class MockedProducer(object):
    def __init__(self):
        self.produced_messages = defaultdict(list)
        self.flushed = False

    def send(self, topic, value=None, key=None):
        self.produced_messages[topic].append((value, key, ))

    def flush(self):
        self.flushed = True
