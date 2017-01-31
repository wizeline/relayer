class RPCContextHandler(object):
    def __init__(self, event_emitter):
        self.event_emitter = event_emitter
        self.kafka_producer_request_logs = []

    def start_request(self):
        self.kafka_producer_request_logs = []

    def emit(self, topic, message, partition_key=None):
        self.event_emitter.emit(topic, message, partition_key)
        # It is important to first emit the message before appending to the log list so if the emit call fails because
        # the messsage is malformed, the final log message doesn't fail for the same reason.
        self.kafka_producer_request_logs.append(message)

    def log(self, message):
        self.kafka_producer_request_logs.append(message)

    def end_request(self, logging_topic, request_log):
        log_entry = {}
        log_entry.update(request_log)
        log_entry['lines'] = self.kafka_producer_request_logs

        self.event_emitter.emit(logging_topic, log_entry)
