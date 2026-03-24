import pytest
from nine_mens_morris.game.actions import Move, Remove

def test_apply_illegal_action_raises_value_error(game, player1):
    assert game.get_current_player() == player1
    illegal_actions = [Move(0,1), Remove(0)]
    for illegal_action in illegal_actions:
        with pytest.raises(ValueError, match='Illegal action'):
            game.apply(illegal_action)
    assert game.get_rounds() == 0

def test_apply_legal_action_passes(game, player1, player2):
    assert game.get_current_player() == player1
    legal_actions = game.legal_actions_for_current_player()
    assert len(legal_actions) > 0
    game.apply(legal_actions[0])
    assert game.get_rounds() == 1
