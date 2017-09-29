from datetime import datetime

from relayer import Relayer, utils
from relayer.logging import logger


def make_rpc_relayer(logging_topic, kafka_hosts=None, **kwargs):

    event_relayer = Relayer(
        logging_topic,
        kafka_hosts=kafka_hosts,
        **kwargs,
    )

    def decorator(function):
        def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            kwargs['relayer'] = event_relayer
            service_response = function(*args, **kwargs)
            request_log = {
                'source': event_relayer.source,
                'logging_topic': logging_topic,
                'date': start_time.isoformat(),
                'service': function.__qualname__,
                'service_time': utils.get_elapsed_time_in_milliseconds(start_time, datetime.utcnow())
            }
            logger.info('rpc_request_decorator', **request_log)
            return service_response
        return wrapper

    # Expose relayer instance
    decorator.instance = event_relayer

    return decorator
