from nine_mens_morris.game.action_generator import ActionGenerator
from nine_mens_morris.game.actions import Action, Remove, Move, Place
from nine_mens_morris.game.player import Player
from nine_mens_morris.game.board import Board
from nine_mens_morris.game.game_state import GameState


class Game:
    def __init__(self, player1: Player, player2: Player, board: Board | None = None):
        self.__player1 = player1
        self.__player2 = player2
        self.__board = board if board is not None else Board()
        self.__current_player = player1
        self.__state = GameState.PLACING
        self.__mills_formed = False     # flag that the last move caused the creation of a mill
        self.__rounds = 0
        self.__action_generator: ActionGenerator = ActionGenerator(self, self.__board)

    def get_action_generator(self) -> ActionGenerator:
        return self.__action_generator

    def get_rounds(self):
        return self.__rounds

    def get_state(self) -> GameState:
        return self.__state

    def set_state(self, new_state: GameState) -> None:
        self.__state = new_state

    def get_mills_formed(self) -> bool:
        return self.__mills_formed

    def get_player_on_position(self, pos_id: int) -> Player | None:
        return self.__board.occupied_by(pos_id)

    def get_player1(self) -> Player:
        return self.__player1

    def get_player2(self) -> Player:
        return self.__player2

    def get_current_player(self) -> Player:
        return self.__current_player

    def get_opposite_player(self) -> Player:
        return self.get_player2() if self.get_current_player() == self.get_player1() \
            else self.get_player1()

    def render_board(self) -> str:
        return str(self.__board)

    def switch_current_player(self) -> None:
        if self.get_current_player() == self.get_player1():
            self.__current_player = self.get_player2()
        else:
            self.__current_player = self.get_player1()

    def game_over(self) -> bool:
        if self.get_state() == GameState.GAME_OVER:
            return True
        return self._is_defeated(self.__player1) or self._is_defeated(self.__player2)

    def _is_defeated(self, player: Player) -> bool:
        if self.get_state() == GameState.PLACING:
            return player.get_pieces_on_board() + player.get_pieces_in_hand() <= 2

        return player.get_pieces_on_board() <= 2 or\
            not self.__action_generator.has_any_move(player)

    def get_winner(self) -> Player | None:
        if self.get_state() == GameState.GAME_OVER:
            p1_defeated = self._is_defeated(self.__player1)
            p2_defeated = self._is_defeated(self.__player2)
            if p1_defeated and not p2_defeated: return self.__player2
            elif p2_defeated and not p1_defeated: return self.__player1
        return None

    def legal_actions_for_current_player(self) -> list[Action]:
        return self.__action_generator.legal_actions()

    def apply(self, action: Action):
        if action not in self.legal_actions_for_current_player():
            raise ValueError("Illegal action")

        match action.kind:
            case "place":
                self._handle_place(action.pos)
            case "move":
                self._handle_move(action.pos_from, action.pos_to)
            case "remove":
                self._handle_remove(action.pos)
            case _:
                raise ValueError(f"Unknown action '{action}'")

        self.__rounds += 1
        if self.__state != GameState.GAME_OVER and self.game_over():
            self.__state = GameState.GAME_OVER

    def _handle_place(self, pos_id: int) -> None:
        self.__board.place_piece(self.get_current_player(), pos_id)
        self.get_current_player().decrement_in_hand()
        self.get_current_player().increment_on_board()

        mill = self.__board.get_mill(pos_id, self.get_current_player())
        if mill is not None and not self.get_current_player().has_had_mill(mill):
            self.__mills_formed = True
            self.get_current_player().add_mill(mill)
        else:
            self.switch_current_player()

        if (self.get_player1().get_pieces_in_hand() == 0 and
                self.get_player2().get_pieces_in_hand() == 0):
            self.__state = GameState.MOVING


    def _handle_move(self, from_pos_id: int, to_pos_id: int) -> None:
        self.__board.move_piece(from_pos_id, to_pos_id, self.get_current_player())

        mill = self.__board.get_mill(to_pos_id, self.get_current_player())
        if mill is not None and not self.get_current_player().has_had_mill(mill):
            self.__mills_formed = True
            self.get_current_player().add_mill(mill)
        else:
            self.switch_current_player()


    def _handle_remove(self, pos_id: int) -> None:
        self.__board.remove_piece(pos_id,
                                  self.get_current_player(), self.get_opposite_player())

        self.__mills_formed = False
        self.get_opposite_player().decrement_on_board()

        if self.game_over():
            self.__state = GameState.GAME_OVER
            return

        self.switch_current_player()

        if self.get_state() != GameState.PLACING:
            self.__state = GameState.JUMPING if self.get_current_player().can_jump() else GameState.MOVING
