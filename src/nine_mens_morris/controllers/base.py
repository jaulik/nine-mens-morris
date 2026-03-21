from __future__ import annotations
from typing import Protocol

from nine_mens_morris.game.actions import Action
from nine_mens_morris.game.game import Game

class Controller(Protocol):
    def choose_action(self, game: Game) -> Action:
        """Return an action for the current player in the given game state."""
