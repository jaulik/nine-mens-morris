from src.game.position import Position

class PositionAlreadyOccupiedError(Exception):
    def __init__(self, position: Position):
        self.position_id = position.get_id()
        self.position_occupied_by_id = position.get_occupied_by().get_id()
        super().__init__(f"Position {self.position_id} is already occupied by player ID: {self.position_occupied_by_id}.")

class InvalidMoveError(Exception):
    def __init__(self, from_position: Position, to_position: Position):
        self.from_pos_id = from_position.get_id()
        self.to_pos_id = to_position.get_id()
        super().__init__(f"Move from position {self.from_pos_id} to position {self.to_pos_id} is not permitted.")

class InvalidPieceRemovalError(Exception):
    def __init__(self, position_id: int, attempted_by: int, actual_owner: int | None):
        message = (f"Cannot remove piece at position {position_id}. "
                   f"Attempted by player {attempted_by}, but position is "
                   f"{'empty' if actual_owner is None else f'occupied by player {actual_owner}'}.")
        super().__init__(message)
        self.position_id = position_id
        self.attempted_by = attempted_by
        self.actual_owner = actual_owner

class PositionOutOfBoundsError(Exception):
    def __init__(self, position_id: int):
        super().__init__(f"Position {position_id} is out of bounds (valid positions are 0–23).")
        self.position_id = position_id
