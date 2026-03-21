from __future__ import annotations

from nine_mens_morris.cli.io import IO
from nine_mens_morris.controllers.base import Controller
from nine_mens_morris.game.actions import Place, Remove, Move
from nine_mens_morris.game.exceptions import *
from nine_mens_morris.game.game import Game
from nine_mens_morris.game.game_state import GameState
from nine_mens_morris.controllers.base import Controller

class GameRunner:
    def __init__(self, game: Game, controller_player1: Controller, controller_player2: Controller, io: IO):
        self.game = game
        self.controller_player1 = controller_player1
        self.controller_player2 = controller_player2
        self.io = io

    def _get_controller_for_current_player(self) -> Controller:
        if self.game.get_current_player() == self.game.get_player1():
            return self.controller_player1
        return self.controller_player2

    def run(self):
        while self.game.get_state() != GameState.GAME_OVER:
            self.io.write(self.game.render_board())
            self.io.write("Current_player: " + self.game.get_current_player().get_name())

            controller = self._get_controller_for_current_player()
            try:
                action = controller.choose_action(self.game, self.io)
                self.game.apply(action)

            except ValueError:
                self.io.write("Error: Invalid input or illegal action. Please enter a valid number.\n")
            except (PositionOutOfBoundsError, PositionAlreadyOccupiedError,
                    InvalidMoveError, InvalidPieceRemovalError) as e:
                self.io.write(f"Invalid action: {e}\n")

        winner = self.game.get_winner()
        if winner:
            self.io.write("GAME OVER! Winner: " + winner.get_name() + " ID: " + str(winner.get_id()))
        else:
            self.io.write("GAME OVER! No winner was determined.")

        return winner
