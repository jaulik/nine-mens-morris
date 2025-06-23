from player import Player
from board import Board
from position import Position
from game_state import GameState

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.__player1 = player1
        self.__player2 = player2
        self.__board = Board()
        self.__current_player = player1
        self.__state = GameState.PLACING

    def get_board_positions(self) -> dict[int, Position]:
        return self.__board.get_board()
    
    def get_player1(self) -> Player:
        return self.__player1
    
    def get_player2(self) -> Player:
        return self.__player2
    
    def get_current_player(self) -> Player:
        return self.__current_player
    
    def switch_current_player(self) -> None:
        if self.get_current_player() == self.get_player1():
            self.__current_player = self.get_player1()
        else:
            self.__current_player = self.get_player2()
