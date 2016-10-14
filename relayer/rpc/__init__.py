from relayer import Relayer, utils
from .rpc_context_handler import RPCContextHandler

from datetime import datetime


def make_rpc_relayer(logging_topic, kafka_hosts=None, topic_prefix='', topic_suffix='', source=''):

    event_relayer = Relayer(logging_topic, RPCContextHandler, kafka_hosts=kafka_hosts,
                            topic_prefix=topic_prefix, topic_suffix=topic_suffix, source=source)
    context = event_relayer.context

    def decorator(function):
        def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            kwargs['relayer'] = event_relayer
            context.start_request()
            service_response = function(*args, **kwargs)
            end_time = datetime.utcnow()
            request_log = {
                'source': event_relayer.source,
                'logging_topic': logging_topic,
                'date': start_time.isoformat(),
                'service': function.__qualname__,
                'service_time': utils.get_elapsed_time_in_milliseconds(start_time, end_time)
            }
            context.end_request(logging_topic, request_log)
            return service_response
        return wrapper
    return decorator
