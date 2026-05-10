from functools import total_ordering
from typing import override
from Node import Node

@total_ordering
class Element:

    def __init__(self, key: int, data: Node):
        self.key: int = key
        self.data: Node = data

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Element):
            return NotImplemented
        return self.key == other.key

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Element):
            return NotImplemented
        return self.key < other.key

    @override
    def __str__(self):
        return f"Element -> {self.key}\t{self.data}"


