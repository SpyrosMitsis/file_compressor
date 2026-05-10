from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Node:
    left: Node | None = None
    right: Node | None = None
    byte_value: int | None = None

    def is_leaf(self) -> bool:
        return self.byte_value is not None
