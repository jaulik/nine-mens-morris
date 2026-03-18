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
        self.__action_generator: ActionGenerator = ActionGenerator(self, board)

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

    def get_all_possible_moves(self, player: Player) -> list[int]:
        moves: list[int] = []

        for from_pos_id in self.__board.positions_occupied_by(player):
            for to_pos_id in self.__board.neighbors_of(from_pos_id):
                if self.__board.occupied_by(to_pos_id) is None:
                    moves.append(to_pos_id)
        return moves

    def game_over(self) -> bool:
        if self.get_state() == GameState.GAME_OVER:
            return True

        opponent = self.get_opposite_player()
        if self.get_state() == GameState.PLACING:
            return (opponent.get_pieces_on_board() + opponent.get_pieces_in_hand()) <= 2

        return opponent.get_pieces_on_board() <= 2 or self.get_all_possible_moves(opponent) == []

    def get_winner(self) -> Player | None:
        if self.get_state() != GameState.GAME_OVER:
            return None
        players = [self.get_player1(), self.get_player2()]
        for player in players:
            if player.get_pieces_on_board() >= 3 and self.get_all_possible_moves(player) != []:
                return player
        return None

    def apply(self, action: Action):
        match action.kind:
            case "place":
                self.play_round(action.kind, action.pos)
            case "move":
                self.play_round(action.kind, action.pos_from, action.pos_to)
            case "remove":
                self.play_round(action.kind, action.pos)
            case _:
                raise ValueError(f"Unknown action '{action}'")

    def legal_actions_for_current_player(self) -> list[Action]:
        return self.__action_generator.legal_actions()

    def play_round(self, action: str, *args) -> None:
        """
        action: "place", "move", "remove"
        args:
          - place:   position_id
          - move:    from_id, to_id
          - remove:  position_id
        """
        if action == "place":
            self._handle_place(args[0])
        elif action == "move":
            self._handle_move(args[0], args[1])
        elif action == "remove":
            self._handle_remove(args[0])
        else:
            raise ValueError(f"Unknown action '{action}'")

        self.__rounds += 1
        if self.__state != GameState.GAME_OVER and self.game_over():
            self.__state = GameState.GAME_OVER


    def _handle_place(self, pos_id: int) -> None:
        if self.get_state() != GameState.PLACING:
            return

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
        valid_states = {GameState.MOVING, GameState.JUMPING}
        if self.get_state() not in valid_states or self.__mills_formed:
            return

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
