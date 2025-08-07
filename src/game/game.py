from src.game.player import Player
from src.game.board import Board
from src.game.game_state import GameState
from src.game.exceptions import *

class Game:
    def __init__(self, player1: Player, player2: Player):
        self.__player1 = player1
        self.__player2 = player2
        self.__board = Board()
        self.__current_player = player1
        self.__state = GameState.PLACING
        self.__mills_formed = False     # flag that the last move caused the creation of a mill
        self.__rounds = 0

    def get_rounds(self):
        return self.__rounds

    def get_state(self) -> GameState:
        return self.__state
    
    def set_state(self, new_state: GameState) -> None:
        self.__state = new_state
    
    def get_player_on_position(self, pos_id: int) -> Player | None:
        return self.__board.get_position(pos_id).get_occupied_by()
    
    def get_player1(self) -> Player:
        return self.__player1
    
    def get_player2(self) -> Player:
        return self.__player2
    
    def get_current_player(self) -> Player:
        return self.__current_player
    
    def get_opposite_player(self) -> Player:
        return self.get_player2() if self.get_current_player() == self.get_player1()\
            else self.get_player1()

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
        if self.get_state() == GameState.PLACING:
            return False

        opponent = self.get_opposite_player()
        return opponent.get_pieces_on_board() <= 2 or self.get_all_possible_moves(opponent) == []

    def get_winner(self) -> Player | None:
        if self.get_state() != GameState.GAME_OVER:
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
        if action == "place" and self.get_state() == GameState.PLACING:
            try:
                pos_id = args[0]
                self.__board.place_piece(self.get_current_player(), pos_id)
                self.get_current_player().decrement_in_hand()
                self.get_current_player().increment_on_board()

                mill = self.__board.get_mill(pos_id, self.get_current_player())
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
            (self.get_state() == GameState.MOVING or self.get_state() == GameState.JUMPING)\
            and not self.__mills_formed:
            try:
                from_pos_id, to_pos_id = args
                self.__board.move_piece(from_pos_id, to_pos_id, self.get_current_player())
                
                mill = self.__board.get_mill(to_pos_id, self.get_current_player())
                if mill is not None and not self.get_current_player().has_had_mill(mill):
                    self.__mills_formed = True
                    self.get_current_player().add_mill(mill)
                else:
                    self.switch_current_player()
            
            except (PositionOutOfBoundsError, PositionAlreadyOccupiedError, InvalidMoveError) as e:
                print(e)

        elif action == "remove":
            try:
                self.__board.remove_piece(args[0],
                                          self.get_current_player(),
                                          self.get_opposite_player())

                self.__mills_formed = False
                self.get_opposite_player().decrement_on_board()
                if self.get_opposite_player().can_jump():
                    self.__state = GameState.JUMPING
                
                self.switch_current_player()

            except (InvalidPieceRemovalError, PositionOutOfBoundsError) as e:
                print(e)
        else:
            raise ValueError(f"Unknown action '{action}'")

        self.__rounds += 1
        if self.game_over():
            self.__state = GameState.GAME_OVER

    def play(self):
        while self.get_state() != GameState.GAME_OVER:
            print(self.__board)
            print("Current_player: ", self.get_current_player().get_name())

            if self.__mills_formed:
                try:
                    pos_id = int(input("Enter position of opponents piece to remove: "))
                    self.play_round("remove", pos_id)
                except ValueError:
                    print("Invalid number.")
            elif self.get_state() == GameState.PLACING:
                try:
                    pos_id = int(input("Enter position where do you want to place your piece: "))
                    self.play_round("place", pos_id)
                except ValueError:
                    print("Invalid number.")
            elif self.get_state() == GameState.MOVING or self.get_state() == GameState.JUMPING:
                try:
                    from_pos_id = int(input("Enter from which position do you want to move your piece: "))
                    to_pos_id = int(input("Enter to which position do you want to place your piece: "))
                    self.play_round("move", from_pos_id, to_pos_id)
                except ValueError:
                    print("Invalid number.")

        winner = self.get_winner()
        if winner:
            print("GAME OVER! Winner: ", winner.get_name(), " ID: ", winner.get_id())
        else:
            print("GAME OVER! No winner was determined.")

        return winner
