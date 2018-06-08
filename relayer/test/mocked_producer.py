from typing import Dict, Any, List, Tuple
from collections import defaultdict


class MockedProducer(object):
    def __init__(self) -> None:
        self.produced_messages: Dict[Any, List[Tuple[Any, ...]]] = defaultdict(list)
        self.flushed = False

    def send(self, topic: str, value: str = None, key: str = None) -> None:
        self.produced_messages[topic].append((value, key))

    def flush(self) -> None:
        self.flushed = True
