
class Position:
    def __init__(self, id: int, neighbors: list[int]):
        self.__id = id
        self.__neighbors = neighbors
        self.__occupied_by: int | None = None   

    def get_id(self) -> int:
        return self.__id

    def get_neighbors(self) -> list[int]:
        return self.__neighbors.copy()

    def get_occupied_by(self) -> int | None:
        return self.__occupied_by

    def set_occupied_by(self, player_id: int | None) -> None:
        self.__occupied_by = player_id

