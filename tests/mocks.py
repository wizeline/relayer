from collections import defaultdict


class MockedProducer(object):
    def __init__(self):
        self.produced_messages = defaultdict(list)
        self.flushed = False

    def send(self, topic, value=None, key=None):
        self.produced_messages[topic].append((value, key, ))

    def flush(self):
        self.flushed = True


class MockedContextHandler(object):
    def __init__(self, emitter):
        self.emitter = emitter

    def emit(self, topic, message, partition_key=None):
        self.topic = topic
        self.message = message
        self.partition_key = partition_key

    def log(self, message):
        self.log_message = message
