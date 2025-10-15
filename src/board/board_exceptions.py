class BoardException(Exception):
    def __init__(self, message="Board exception"):
        self.__message = message

    def __str__(self):
        return self.__message

class PositionUnavailableException(BoardException):
    def __init__(self):
        super().__init__("Position already occupied by a piece")

class OutOfBoundsException(BoardException):
    def __init__(self):
        super().__init__("Position out of bounds")