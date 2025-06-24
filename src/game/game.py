from player import Player
from board import Board
from position import Position
from game_state import GameState
from exceptions import *

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.__player1 = player1
        self.__player2 = player2
        self.__board = Board()
        self.__current_player = player1
        self.__state = GameState.PLACING
        self.__mills_formed = False     # flag that the last move caused the creation of a mill


    # def get_board_positions(self) -> dict[int, Position]:
    #     return self.__board.get_board()

    def get_state(self) -> GameState:
        return self.__state
    
    def get_player1(self) -> Player:
        return self.__player1
    
    def get_player2(self) -> Player:
        return self.__player2
    
    def get_current_player(self) -> Player:
        return self.__current_player
    
    def get_opposite_player(self) -> Player:
        return self.get_player1() if self.get_current_player() == self.get_player1()\
            else self.get_player2()

    def switch_current_player(self) -> None:
        if self.get_current_player() == self.get_player1():
            self.__current_player = self.get_player1()
        else:
            self.__current_player = self.get_player2()




    def play(self, action: str, *args) -> None:
        """
        action: "place", "move", "remove"
        args:
          - place:   position_id
          - move:    from_id, to_id
          - remove:  position_id
        """
        if action == "place":
            try:
                pos_id = args[0]
                self.place_piece(pos_id)
                self.get_current_player().decrement_in_hand()
                self.get_current_player().increment_on_board()

                if self.__board.is_mill(pos_id, self.get_current_player().get_id()):
                    self.__mills_formed = True
                else:
                    self.__mills_formed = False
                self.switch_current_player()
            
            except (PositionOutOfBoundsError, PositionAlreadyOccupiedError) as e:
                print(e)

        elif action == "move":
            try:
                from_pos_id, to_pos_id = args
                self.move_piece(from_pos_id, to_pos_id)
                if self.__board.is_mill(to_pos_id, self.get_current_player().get_id()):
                    self.__mills_formed = True
                else:
                    self.__mills_formed = False
                self.switch_current_player()
            
            except (PositionOutOfBoundsError, PositionAlreadyOccupiedError, InvalidMoveError) as e:
                print(e)

        elif action == "remove":
            try:
                self.remove_piece(args[0])
                self.__mills_formed = False
                self.switch_current_player()
                self.get_opposite_player().decrement_on_board()

            except (InvalidPieceRemovalError, PositionOutOfBoundsError) as e:
                print(e)
        else:
            raise ValueError(f"Unknown action '{action}'")


    def place_piece(self, position_id: int) -> None:
        board = self.__board
        if not (0 <= position_id <= 23):
            raise PositionOutOfBoundsError(position_id)
        board.place_piece(self.get_current_player(), position_id)
        

    def move_piece(self, from_pos_id: int, to_pos_id: int) -> None:
        if not (0 <= from_pos_id <= 23 and 0 <= to_pos_id <= 23):
            raise PositionOutOfBoundsError(from_pos_id
                                           if from_pos_id < 0 or from_pos_id > 23 else to_pos_id)

        board = self.__board
        from_pos = board.get_position(from_pos_id)
        to_pos = board.get_position(to_pos_id)

        if from_pos.get_occupied_by() != self.__current_player.get_id():
            raise InvalidMoveError(from_pos, to_pos)
        
        board.move_piece(from_pos_id, to_pos_id)

    def remove_piece(self, position_id: int) -> None:
        if not (0 <= position_id <= 23):
            raise PositionOutOfBoundsError(position_id)
        
        target_pos = self.__board.get_position(position_id)
        occupied_by = target_pos.get_occupied_by()

        if occupied_by is None or occupied_by == self.get_current_player().get_id():
            raise InvalidPieceRemovalError(position_id, self.get_current_player().get_id(),
                                           None if occupied_by is None else occupied_by.get_id())

        self.__board.remove_piece(position_id,
                                  self.get_current_player().get_id(),
                                  self.get_opposite_player().get_id())
