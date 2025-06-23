
class Player:
    def __init__(self, name: str, id: int):
        self.__name = name
        self.__id = id
        self.__pieces_on_board = 0
        self.__pieces_in_hand = 9

    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> int:
        return self.__id

    def get_pieces_on_board(self) -> int:
        return self.__pieces_on_board

    def get_pieces_in_hand(self) -> int:
        return self.__pieces_in_hand

    def can_jump(self) -> bool:
        return self.get_pieces_on_board() <= 3 and self.get_pieces_in_hand() == 0
