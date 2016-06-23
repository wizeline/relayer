class MockedContextHandler(object):
    def __init__(self, emitter):
        self.emitter = emitter

    def emit(self, topic, message, partition_key=None):
        self.topic = topic
        self.message = message
        self.partition_key = partition_key

    def log(self, message):
        self.log_message = message
