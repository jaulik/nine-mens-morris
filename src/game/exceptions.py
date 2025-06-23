from position import Position

class PositionAlreadyOccupiedError(Exception):
    def __init__(self, position: Position):
        self.position_id = position.get_id()
        self.position_occupied_by = position.get_occupied_by()
        super().__init__(f"Position {self.position_id} is already occupied by player {self.position_occupied_by}.")

class InvalidPieceRemovalError(Exception):
    def __init__(self, position_id: int, attempted_by: int, actual_owner: int | None):
        message = (f"Cannot remove piece at position {position_id}. "
                   f"Attempted by player {attempted_by}, but position is "
                   f"{'empty' if actual_owner is None else f'occupied by player {actual_owner}'}.")
        super().__init__(message)
        self.position_id = position_id
        self.attempted_by = attempted_by
        self.actual_owner = actual_owner
