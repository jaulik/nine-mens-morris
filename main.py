from src.game.player import Player
from src.game.game import Game

from src.db.manage_db import add_player, start_game, end_game, get_statistics

if __name__ == "__main__":
    # TODO: if player already exists enter name and id and proceed (SELECT)

    print("Here rules and instruction should be printed.")
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
