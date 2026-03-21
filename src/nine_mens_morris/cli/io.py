from __future__ import annotations
from typing import Protocol


class IO(Protocol):
    def read_int(self, prompt: str) -> int:
        ...
    def write(self, text: str) -> None:
        ...
