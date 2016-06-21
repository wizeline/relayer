from flask import _app_ctx_stack as stack


class FlaskContextHandler(object):
    def __init__(self, event_emitter):
        self.event_emitter = event_emitter

    def start_request(self):
        ctx = stack.top
        ctx.kafka_producer_request_logs = []

    def emit(self, topic, message, partition_key=None):
        ctx = stack.top
        self.event_emitter.emit(topic, message, partition_key)
        # It is important to first emit the message before appending to the log list so if the emit call fails because
        # the messsage is malformed, the final log message doesn't fail for the same reason.
        ctx.kafka_producer_request_logs.append(message)

    def log(self, message):
        ctx = stack.top
        ctx.kafka_producer_request_logs.append(message)

    def end_request(self, logging_topic, request_log):
        ctx = stack.top

        log_entry = {}
        log_entry.update(request_log)
        log_entry['lines'] = ctx.kafka_producer_request_logs

        self.event_emitter.emit(logging_topic, log_entry)
        self.event_emitter.flush()
