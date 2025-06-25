from src.game.player import Player

class Position:
    def __init__(self, id: int, neighbors: list[int]):
        self.__id = id
        self.__neighbors = neighbors
        self.__occupied_by: Player | None = None   

    def get_id(self) -> int:
        return self.__id

    def get_neighbors(self) -> tuple[int, ...]:
        return tuple(self.__neighbors)

    # TODO: unmodifiable
    def get_occupied_by(self) -> Player | None:
        return self.__occupied_by

    def set_occupied_by(self, player: Player | None) -> None:
        self.__occupied_by = player
