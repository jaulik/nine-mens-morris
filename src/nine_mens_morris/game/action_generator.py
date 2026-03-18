from __future__ import annotations

from typing import TYPE_CHECKING
from nine_mens_morris.game.actions import Action, Remove, Move, Place
from nine_mens_morris.game.board import Board
from nine_mens_morris.game.game_state import GameState
from nine_mens_morris.game.player import Player

if TYPE_CHECKING:
    from nine_mens_morris.game.game import Game

class ActionGenerator:
    def __init__(self, game: "Game", board: Board):
        self.__game = game
        self.__board = board

    def legal_actions(self) -> list[Action]:
        return self.legal_actions_for(self.__game.get_current_player())

    def legal_actions_for(self, player: Player) -> list[Action]:
        is_current_turn = (player == self.__game.get_current_player())
        opponent = (self.__game.get_opposite_player() if is_current_turn
                    else self.__game.get_current_player())
        if self.__game.get_mills_formed():
            # waiting for stone removal
            if not is_current_turn:
                return []
            opponent_positions = self.__board.positions_occupied_by(opponent)
            not_in_mill = [pos for pos in opponent_positions\
                           if not self.__board.is_in_mill(pos, opponent)]
            if len(not_in_mill) > 0:
                return [Remove(pos) for pos in not_in_mill]
            # only allow removing stones that are part of opponents mill
            # if opponent has no stones that are not a part of a mill
            return [Remove(pos) for pos in opponent_positions]

        if self.__game.get_state() == GameState.PLACING:
            return [Place(pos) for pos in self.__board.empty_positions()]

        if self.__game.get_state() in (GameState.MOVING, GameState.JUMPING):
            actions: list[Action] = []
            empty_positions = self.__board.empty_positions()

            for from_pos in self.__board.positions_occupied_by(player):
                if player.can_jump():
                    for to_pos in empty_positions:
                        actions.append(Move(from_pos, to_pos))
                else:
                    for to_pos in self.__board.neighbors_of(from_pos):
                        if self.__board.occupied_by(to_pos) is None:
                            actions.append(Move(from_pos, to_pos))
            return actions
        return []
