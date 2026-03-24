def test_smoke_game_creation(game):
    assert game is not None
    actions = game.get_action_generator().legal_actions()
    assert len(actions) > 0
