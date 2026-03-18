from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class Place:
    pos: int
    kind: Literal["place"] = "place"

@dataclass(frozen=True)
class Move:
    pos_from: int
    pos_to: int
    kind: Literal["move"] = "move"

@dataclass(frozen=True)
class Remove:
    pos: int
    kind: Literal["remove"] = "remove"

Action = Place | Move | Remove
