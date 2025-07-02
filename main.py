from src.game.player import Player
from src.game.game import Game

from src.db.manage_db import add_player, start_game, end_game, get_statistics

if __name__ == "__main__":
    # TODO: if player already exists enter name and id and proceed (SELECT)

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
    name1 = input("Enter name of player 1: ")
    id1 = add_player(name1)
    print("Your ID is: ", id1)
    player1 = Player(name1, id1)
    
    name2 = input("Enter name of player 2: ")
    id2 = add_player(name2)
    print("Your ID is: ", id2)
    player2 = Player(name2, id2)

    game_id = start_game(id1, id2)
    game = Game(player1, player2)
    
    winner = game.play()
    end_game(winner.get_id(), game.get_rounds(), game_id)
