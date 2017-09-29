import structlog


logger = structlog.get_logger('wizeline.lib.relayer')


def log_deprecation_notice(source=None):
    logger.warn('deprecation_notice', source=source)
