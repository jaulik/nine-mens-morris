from src.game.game import Game
from src.game.game_state import GameState

class GameRunner:
    def __init__(self, game: Game):
        self.game = game

    def run(self):
        while self.game.get_state() != GameState.GAME_OVER:
            print(self.game.get_board())
            print("Current_player: ", self.game.get_current_player().get_name())

            if self.game.get_mills_formed():
                try:
                    pos_id = int(input("Enter position of opponents piece to remove: "))
                    self.game.play_round("remove", pos_id)
                except ValueError:
                    print("Invalid number.")
            elif self.game.get_state() == GameState.PLACING:
                try:
                    pos_id = int(input("Enter position where do you want to place your piece: "))
                    self.game.play_round("place", pos_id)
                except ValueError:
                    print("Invalid number.")
            elif self.game.get_state() == GameState.MOVING or self.game.get_state() == GameState.JUMPING:
                try:
                    from_pos_id = int(input("Enter from which position do you want to move your piece: "))
                    to_pos_id = int(input("Enter to which position do you want to place your piece: "))
                    self.game.play_round("move", from_pos_id, to_pos_id)
                except ValueError:
                    print("Invalid number.")

        winner = self.game.get_winner()
        if winner:
            print("GAME OVER! Winner: ", winner.get_name(), " ID: ", winner.get_id())
        else:
            print("GAME OVER! No winner was determined.")

        return winner
