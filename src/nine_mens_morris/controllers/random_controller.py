from __future__ import annotations

import random

from nine_mens_morris.game.actions import Action
from nine_mens_morris.game.game import Game

class RandomController:
    def choose_action(self, game: Game) -> Action:
        actions = game.legal_actions_for_current_player()
        if not actions:
            raise RuntimeError("No legal actions available for current player.")
        return random.choice(actions)
