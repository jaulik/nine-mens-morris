from __future__ import annotations

from nine_mens_morris.cli.io import IO
from nine_mens_morris.game.actions import Action, Remove, Move, Place
from nine_mens_morris.game.game import Game
from nine_mens_morris.game.game_state import GameState

class HumanController:
    def choose_action(self, game: Game, io: IO) -> Action:
        if game.get_mills_formed():
            pos_id = io.read_int("Enter position of opponents piece to remove: ")
            return Remove(pos_id)

        if game.get_state() == GameState.PLACING:
            pos_id = io.read_int("Enter position where do you want to place your piece: ")
            return Place(pos_id)

        if game.get_state() in {GameState.MOVING, GameState.JUMPING}:
            from_pos_id = io.read_int("Enter from which position do you want to move your piece: ")
            to_pos_id = io.read_int("Enter to which position do you want to place your piece: ")
            return Move(from_pos_id, to_pos_id)

        raise RuntimeError(f"Unsupported state for human input: {game.get_state()}")
