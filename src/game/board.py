from position import Position
from exceptions import *

# Positions 0–23 correspond to points on the game board.
# Each position knows its neighbors - that is, where a piece can be moved.
# 
#    0--------1--------2
#    |        |        |
#    |   3----4----5   |
#    |   |    |    |   |
#    |   |  6-7-8  |   |
#    |   |  |   |  |   |
#    9--10-11   12-13-14
#    |   |  |   |  |   |
#    |   | 15-16-17|   |
#    |   |    |    |   |
#    |  18---19---20   |
#    |        |        |
#   21-------22-------23

MILLS: list[list[int]] = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
         [0, 9, 21], [3, 10, 18], [6, 11, 15],
         [1, 4, 7], [16, 19, 22], [8, 12, 17],
         [5, 13, 20], [2, 14, 23], [9, 10, 11],
         [12, 13, 14], [15, 16, 17], [18, 19, 20],
         [21, 22, 23]]


class Board:
    def __init__(self):
        self.__positions = self.initialize_positions()

    def initialize_positions(self) -> dict[int, Position]:
                return {
            0: Position(0, [1, 9]),
            1: Position(1, [0, 2, 4]),
            2: Position(2, [1, 14]),
            3: Position(3, [4, 10]),
            4: Position(4, [1, 3, 5, 7]),
            5: Position(5, [4, 13]),
            6: Position(6, [7, 11]),
            7: Position(7, [4, 6, 8]),
            8: Position(8, [7, 12]),
            9: Position(9, [0, 10, 21]),
            10: Position(10, [3, 9, 11, 18]),
            11: Position(11, [6, 10, 15]),
            12: Position(12, [8, 13, 17]),
            13: Position(13, [5, 12, 14, 20]),
            14: Position(14, [2, 13, 23]),
            15: Position(15, [11, 16]),
            16: Position(16, [15, 17, 19]),
            17: Position(17, [12, 16]),
            18: Position(18, [10, 19]),
            19: Position(19, [16, 18, 20, 22]),
            20: Position(20, [13, 19]),
            21: Position(21, [9, 22]),
            22: Position(22, [19, 21, 23]),
            23: Position(23, [14, 22]),
        }

    def get_board(self) -> dict[int, Position]:
        return self.__positions.copy()
    
    def get_position(self, position_id: int) -> Position:
         return self.get_board()[position_id]

    def place_piece(self, player_id: int, position_id: int) -> None:
        position = self.get_position(position_id)

        if position.get_occupied_by() is not None:
            raise PositionAlreadyOccupiedError(position)

        position.set_occupied_by(player_id)


    def move_piece(self, from_pos_id: int, to_pos_id: int) -> None:
        from_pos = self.get_position(from_pos_id)
        to_pos = self.get_position(to_pos_id)

        if to_pos.get_occupied_by() is not None:
            raise PositionAlreadyOccupiedError(to_pos)
    
        to_pos.set_occupied_by(from_pos.get_occupied_by())
        from_pos.set_occupied_by(None)

    def remove_piece(self, position_id: int, player_id: int, opponent_id) -> None:
        position = self.get_position(position_id)
        occupied_by = position.get_occupied_by()
        if occupied_by != opponent_id:
            raise InvalidPieceRemovalError(position_id, player_id, occupied_by)
        position.set_occupied_by(None)

    def is_mill(self, position_id: int, player_id: int) -> bool:
        for mill in MILLS:
             if position_id in mill and\
                all(self.get_position(pos_id).get_occupied_by() == player_id for pos_id in mill):
                       return True
        return False
        
