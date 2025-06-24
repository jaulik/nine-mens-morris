
class Player:
    def __init__(self, name: str, id: int):
        self.__name = name
        self.__id = id
        self.__pieces_on_board = 0
        self.__pieces_in_hand = 9

    def __eq__(self, other): 
        if not isinstance(other, Player):
            return False
        
        return self.get_id == other.get_id and self.get_name == other.get_name

    def __hash__(self):
        return hash(self.get_id, self.get_name)

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

    def decrement_on_board(self):
        self.__pieces_on_board -= 1

    def increment_on_board(self):
        self.__pieces_on_board += 1

    def decrement_in_hand(self):
        self.__pieces_in_hand -= 1
