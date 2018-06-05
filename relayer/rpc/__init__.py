from typing import Any, Callable

from datetime import datetime

from relayer import Relayer, utils
from relayer.logging import logger


def make_rpc_relayer(
    logging_topic: str,
    kafka_hosts: str = '',
    **kwargs: str
) -> Callable[..., Any]:

    event_relayer = Relayer(
        logging_topic,
        kafka_hosts=kafka_hosts,
        **kwargs,
    )

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Callable[..., Any]:
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
    # Adding attributes to Callable instances is not supported by mypy yet.
    # This is the issue tracking these scenarios: https://github.com/python/mypy/issues/2087
    decorator.instance = event_relayer  # type: ignore

    return decorator
