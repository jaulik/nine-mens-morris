from nine_mens_morris.game.actions import Action, Remove, Move, Place
from nine_mens_morris.game.board import Board
from nine_mens_morris.game.game import Game
from nine_mens_morris.game.game_state import GameState


class ActionGenerator:
    def __init__(self, game: Game, board: Board):
        self.__game = game
        self.__board = board

    def legal_actions(self) -> list[Action]:
        if self.__game.get_mills_formed():
            opponent_positions = self.__board.positions_occupied_by(self.__game.get_opposite_player())
            not_in_mill = [pos for pos in opponent_positions if
                           not self.__board.is_in_mill(pos, self.__game.get_opposite_player())]

            if len(not_in_mill) > 0:
                return [Remove(pos) for pos in not_in_mill]
            # only allow removing stones that are part of opponents mill
            # if opponent has no stones that are not a part of a mill
            return [Remove(pos) for pos in opponent_positions]

        if self.__game.get_state() == GameState.PLACING:
            return [Place(pos) for pos in self.__board.empty_positions()]

        if self.__game.get_state() == GameState.MOVING or\
                self.__game.get_state() == GameState.JUMPING:
            actions: list[Action] = []

            for from_pos in (self.__board.
                    positions_occupied_by(self.__game.get_current_player())):

                if self.__game.get_current_player().can_jump():
                    empty_positions = self.__board.empty_positions()
                    for to_pos in empty_positions:
                        actions.append(Move(from_pos, to_pos))
                else:
                    for to_pos in self.__board.neighbors_of(from_pos):
                        if self.__board.occupied_by(to_pos) is None:
                            actions.append(Move(from_pos, to_pos))

            return actions
        return []
