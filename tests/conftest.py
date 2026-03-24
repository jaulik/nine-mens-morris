import pytest
from nine_mens_morris.game.game import Game
from nine_mens_morris.game.player import Player


@pytest.fixture
def player1():
    return Player('Player 1', 1)

@pytest.fixture
def player2():
    return Player('Player 2', 2)

@pytest.fixture
def game(player1, player2):
    return Game(player1, player2)
