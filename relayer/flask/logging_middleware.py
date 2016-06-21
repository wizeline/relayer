from datetime import datetime


class LoggingMiddleware(object):
    def __init__(self, app, wsgi_app, context, logging_topic):
        self.app = app
        self.wsgi_app = wsgi_app
        self.context = context
        self.logging_topic = logging_topic

    def __call__(self, environ, start_response):
        with self.app.app_context():
            start_time = datetime.utcnow()
            status_code = None
            content_length = None

            self.context.start_request()

            def logging_start_response(status, response_headers, exc_info=None):
                nonlocal status_code, content_length
                status_code = int(status.partition(' ')[0])
                for name, value in response_headers:
                    if name.lower() == 'content-length':
                        content_length = int(value)
                        break
                return start_response(status, response_headers, exc_info)

            response = self.wsgi_app(environ, logging_start_response)

            if content_length is None:
                content_length = len(b''.join(response))

            elapsed_time = datetime.utcnow() - start_time
            elapsed_time_milliseconds = elapsed_time.microseconds / 1000.0 + elapsed_time.seconds * 1000

            request_log = {
                'date': start_time.isoformat(),
                'user_agent': environ.get('HTTP_USER_AGENT'),
                'method': environ.get('REQUEST_METHOD'),
                'path': environ.get('PATH_INFO'),
                'query_string': environ.get('QUERY_STRING'),
                'remote_addr': environ.get('REMOTE_ADDR'),
                'status': status_code,
                'content_length': content_length,
                'request_time': elapsed_time_milliseconds
            }

            self.context.end_request(self.logging_topic, request_log)

            return response
