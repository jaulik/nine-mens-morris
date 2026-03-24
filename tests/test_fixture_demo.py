def test_game_starts_with_player1(game, player1, player2):
    assert game.get_current_player() == player1
    assert game.get_opposite_player() == player2
