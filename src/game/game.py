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
            self.__current_player = self.get_player2()
        else:
            self.__current_player = self.get_player1()


    def get_all_possible_moves(self, player: Player) -> list[int]:
        pieces_id = []
        for _, pos in self.__board.get_board().items():
            if pos.get_occupied_by() == player:
                for neighbor_id in pos.get_neighbors():
                    if self.__board.get_position(neighbor_id).get_occupied_by() is None:
                        pieces_id.append(neighbor_id)

        return pieces_id


    def game_over(self) -> bool:
        player1 = self.get_player1()
        player2 = self.get_player2()

        return (player1.get_pieces_in_hand() == 0 and player1.get_pieces_on_board() <= 2) or\
        (player2.get_pieces_in_hand() == 0 and player2.get_pieces_on_board() <= 2) or\
        self.get_all_possible_moves(player1) == [] or self.get_all_possible_moves(player2) == []

    def get_winner(self) -> Player | None:
        if self.__state != GameState.GAME_OVER:
            return None
        players = [self.get_player1(), self.get_player2()]
        for player in players:
            if player.get_pieces_on_board() >= 3 and self.get_all_possible_moves(player) != []:
                return player
        return None


    def play_round(self, action: str, *args) -> None:
        """
        action: "place", "move", "remove"
        args:
          - place:   position_id
          - move:    from_id, to_id
          - remove:  position_id
        """
        if action == "place" and self.__state == GameState.PLACING and not self.__mills_formed:
            try:
                pos_id = args[0]
                self.__board.place_piece(self.get_current_player(), pos_id)
                self.get_current_player().decrement_in_hand()
                self.get_current_player().increment_on_board()

                mill = self.__board.get_mill(pos_id, self.get_current_player().get_id())
                if mill is not None and not self.get_current_player().has_had_mill(mill):
                    self.__mills_formed = True
                    self.get_current_player().add_mill(mill)
                else:
                    self.switch_current_player()
            
            except (PositionOutOfBoundsError, PositionAlreadyOccupiedError) as e:
                print(e)
            finally:
                if self.get_player1().get_pieces_in_hand() == 0 and\
                    self.get_player2().get_pieces_in_hand() == 0:
                    self.__state = GameState.MOVING

        elif action == "move" and\
            (self.__state == GameState.MOVING or self.__state == GameState.JUMPING)\
            and not self.__mills_formed:
            try:
                from_pos_id, to_pos_id = args
                self.__board.move_piece(from_pos_id, to_pos_id, self.get_current_player())
                
                mill = self.__board.get_mill(pos_id, self.get_current_player().get_id())
                if mill is not None and not self.get_current_player().has_had_mill(mill):
                    self.__mills_formed = True
                    self.get_current_player().add_mill(mill)
                else:
                    self.switch_current_player()
            
            except (PositionOutOfBoundsError, PositionAlreadyOccupiedError, InvalidMoveError) as e:
                print(e)

        elif action == "remove" and self.__mills_formed:
            try:
                self.__board.remove_piece(args[0],
                                          self.get_current_player(),
                                          self.get_opposite_player())

                self.__mills_formed = False
                self.get_opposite_player().decrement_on_board()
                if self.get_opposite_player().can_jump():
                    self.__state = GameState.JUMPING
                
                self.switch_current_player()
                self.get_opposite_player().decrement_on_board()

            except (InvalidPieceRemovalError, PositionOutOfBoundsError) as e:
                print(e)
        else:
            raise ValueError(f"Unknown action '{action}'")

        if self.game_over():
            self.__state = GameState.GAME_OVER

