from nine_mens_morris.game.game import Game
from nine_mens_morris.game.player import Player


def test_smoke_game_creation():
    p1, p2 = Player("p1", 1), Player("p2", 2)
    game = Game(p1, p2)
    assert game is not None
    actions = game.get_action_generator().legal_actions()
    assert len(actions) > 0
