import pytest
from nine_mens_morris.game.actions import Place, Move
from nine_mens_morris.game.game_state import GameState

def test_non_current_player_has_no_move(game, player1, player2):
    assert game.get_current_player() == player1
    assert game.get_action_generator().legal_actions_for(player2) == []

def test_current_player_has_24_actions_in_the_beginning(game, player1):
    assert len(game.legal_actions_for_current_player()) == 24

def test_only_place_actions_in_placing(game, player1):
    assert game.get_state() == GameState.PLACING
    actions = game.legal_actions_for_current_player()
    assert len(actions) > 0
    assert all(isinstance(action, Place) for action in actions)

def test_player_changes_after_legal_action(game, player1, player2):
    assert game.get_current_player() == player1
    legal_actions = game.legal_actions_for_current_player()
    assert len(legal_actions) > 0
    game.apply(legal_actions[0])
    assert game.get_current_player() == player2

def test_player_doesnt_changes_after_illegal_action(game, player1, player2):
    assert game.get_current_player() == player1
    illegal_action = Move(0,1)
    with pytest.raises(ValueError, match='Illegal action'):
        game.apply(illegal_action)
    assert game.get_current_player() == player1
