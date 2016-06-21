from uuid import UUID


class RelayerError(Exception):
    pass


class NonJSONSerializableMessageError(RelayerError):
    pass


class ConfigurationError(RelayerError):
    def __init__(self):
        super().__init__('Cannot create relayer object if no kafka hosts are provided')


class UnsupportedPartitionKeyTypeError(RelayerError):
    def __init__(self, provided_type):
        super().__init__('Unsuported partition key type provided, got {}, expected {} or {}'.format(
            provided_type.__name__, str.__name__, UUID.__name__))
