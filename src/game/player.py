
class Player:
    def __init__(self, name: str, id: int):
        self.__name = name
        self.__id = id
        self.__pieces_on_board = 0
        self.__pieces_in_hand = 9
        # The mill cannot be in the same place twice (The player cannot tear it down and rebuild it in the same place).
        self.__past_mills: set[frozenset[int]] = set()   # set of frozenset of int

    def __eq__(self, other): 
        if not isinstance(other, Player):
            return False
        
        return self.get_id() == other.get_id() and self.get_name() == other.get_name()

    def __hash__(self):
        return hash((self.get_id(), self.get_name()))

    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> int:
        return self.__id

    def get_pieces_on_board(self) -> int:
        return self.__pieces_on_board

    def get_pieces_in_hand(self) -> int:
        return self.__pieces_in_hand

    def can_jump(self) -> bool:
        return self.get_pieces_on_board() == 3 and self.get_pieces_in_hand() == 0

    def decrement_on_board(self):
        self.__pieces_on_board -= 1

    def increment_on_board(self):
        self.__pieces_on_board += 1

    def decrement_in_hand(self):
        self.__pieces_in_hand -= 1

    def add_mill(self, mill: list[int]):
        self.__past_mills.add(frozenset(mill))

    def has_had_mill(self, mill: list[int]) -> bool:
        return frozenset(mill) in self.__past_mills
