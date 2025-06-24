from enum import Enum

class GameState(Enum):
    PLACING = 1
    MOVING = 2
    JUMPING = 3
    GAME_OVER = 4
