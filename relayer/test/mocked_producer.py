from collections import defaultdict


class MockedProducer(object):
    def __init__(self) -> None:
        self.produced_messages = defaultdict(list)  # type: Dict[Any, List[Tuple[Any, ...]]]
        self.flushed = False

    def send(self, topic: str, value: str = None, key: str = None) -> None:
        self.produced_messages[topic].append((value, key))

    def flush(self) -> None:
        self.flushed = True
