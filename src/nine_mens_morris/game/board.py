from nine_mens_morris.game.player import Player
from nine_mens_morris.game.exceptions import *

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
                return {0: Position(0, [1, 9]),
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
                        23: Position(23, [14, 22])
                        }

    def _position(self, position_id: int) -> Position:
        if not (0 <= position_id <= 23):
            raise PositionOutOfBoundsError(position_id)
        return self.__positions[position_id]

    def occupied_by(self, position_id: int) -> Player | None:
        return self._position(position_id).get_occupied_by()

    def neighbors_of(self, position_id: int) -> tuple[int, ...]:
        return self._position(position_id).get_neighbors()

    def positions_occupied_by(self, player: Player) -> tuple[int, ...]:
        return tuple(
            pid for pid, pos in self.__positions.items()
            if pos.get_occupied_by() == player
        )

    def empty_positions(self) -> tuple[int, ...]:
        return tuple(pid for pid in range(24) if self.occupied_by(pid) is None)

    def place_piece(self, player: Player, position_id: int) -> None:
        self._position(position_id).set_occupied_by(player)

    def move_piece(self, from_pos_id: int, to_pos_id: int, curr_player: Player) -> None:
        from_pos = self._position(from_pos_id)
        to_pos = self._position(to_pos_id)

        to_pos.set_occupied_by(from_pos.get_occupied_by())
        from_pos.set_occupied_by(None)

    def remove_piece(self, position_id: int, curr_player: Player, opponent: Player) -> None:
        # If opponent has at least one stone NOT in a mill, player cannot remove a stone in a mill.
        opponent_positions = self.positions_occupied_by(opponent)
        opponent_has_not_in_mill = any(not self.is_in_mill(pid, opponent) for pid in opponent_positions)
        if opponent_has_not_in_mill and self.is_in_mill(position_id, opponent):
            raise InvalidPieceRemovalError(position_id, curr_player.get_id(), opponent.get_id())

        self._position(position_id).set_occupied_by(None)

    def is_in_mill(self, position_id: int, opponent: Player) -> bool:
        return any(position_id in mill and\
                   all(self.occupied_by(pid) == opponent for pid in mill)\
                   for mill in MILLS)


    def get_mill(self, position_id: int, player: Player) -> list[int] | None:
        for mill in MILLS:
             if position_id in mill and\
                all(self._position(pos_id).get_occupied_by() == player for pos_id in mill):
                       return mill
        return None


    def __str__(self):
        def f(i):
            pos = self._position(i)
            occ = pos.get_occupied_by()
            val = occ.get_id() if occ else "X"
            return f"{i}:{val}"

        p = [f(i) for i in range(24)]

        return f"""
# {p[0]} ------------ {p[1]} ------------ {p[2]}
#  |               |                  |
#  |   {p[3]}--------{p[4]} -------- {p[5]}    |
#  |    |          |             |    |
#  |    |    {p[6]}--{p[7]} -- {p[8]}     |    |
#  |    |     |           |      |    |
# {p[9]}--{p[10]}--{p[11]}       {p[12]}--{p[13]}--{p[14]}
#  |    |      |           |     |    |
#  |    |    {p[15]}--{p[16]}--{p[17]}    |    |
#  |    |            |           |    |
#  |   {p[18]}--------{p[19]}--------{p[20]}   |
#  |                |                 |
# {p[21]}------------{p[22]}------------ {p[23]}
""".strip()



# 0:X ------------ 1:X ------------ 2:X
#  |               |                  |
#  |   3:X--------4:X -------- 5:X    |
#  |    |          |             |    |
#  |    |    6:X--7:X -- 8:X     |    |
#  |    |     |           |      |    |
# 9:X--10:X--11:X       12:X--13:X--14:X
#  |    |      |           |     |    |
#  |    |     15:X--16:X--17:X   |    |
#  |    |            |           |    |
#  |   18:X--------19:X--------20:X   |
#  |                |                 |
# 21:X------------22:X------------ 23:X