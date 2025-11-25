from src.game.player import Player
from src.game.game import Game

from src.db.manage_db import add_player, start_game, end_game, get_statistics, get_player_id_by_name

if __name__ == "__main__":

    print("""
Welcome to Nine Men's Morris!
Game Rules & Instructions:

    Objective:
    - Reduce your opponent to fewer than three pieces or block all their possible moves.
    - If you achieve this, you win the game!

    Game Phases:
    - Placing: Players take turns placing one of their 9 pieces on any empty position.
    - Moving: When no pieces remain in hand, move pieces to adjacent empty positions.
    - Jumping: If a player has only three pieces left on board, they can "jump" to any empty position.

    Mills:
    - A mill is formed when three of your pieces align in a straight line (horizontal or vertical).
    - When you create a mill, you may remove one of your opponent's pieces.
    - You cannot remove pieces that are currently part of a mill.

    Game Over:
    - The game ends when a player has fewer than 3 pieces or no legal moves.
    - The other player is declared the winner.

    Additional:
    - Positions are numbered from 0 to 23.
    - The game will indicate whose turn it is.
    - Follow the prompts to continue playing.
    - Remember your assigned ID.

    Enjoy the game and let's begin!
    """)

    print("---------------------------------------------")

    def login_player(player_number: int) -> Player:
        while True:
            name = input(f"Enter name of player {player_number}: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue

            existing_id = get_player_id_by_name(name)
            if existing_id is None:
                new_player_id = add_player(name)
                print(f" -> New player created. Your ID is: {new_player_id}")
                return Player(name, new_player_id)

            print(f" -> Welcome back, {name}! Your ID is {existing_id}")
            return Player(name, existing_id)

    player1 = login_player(1)
    while True:
        player2 = login_player(2)
        if player1.get_id() == player2.get_id():
            print("Player 2 cannot be the same as Player 1. Please login as a different user.")
        else:
            break

    game_id = start_game(player1.get_id(), player2.get_id())
    game = Game(player1, player2)
    
    winner = game.play()
    end_game(winner.get_id() if winner else None, game.get_rounds(), game_id)
