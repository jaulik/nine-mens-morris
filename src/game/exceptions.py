from position import Position

class PositionAlreadyOccupiedError(Exception):
    def __init__(self, position: Position):
        self.position_id = position.get_id()
        self.position_occupied_by = position.get_occupied_by()
        super().__init__(f"Position {self.position_id} is already occupied by player {self.position_occupied_by}.")

