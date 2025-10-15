class GameException(Exception):
    def __init__(self, message="Game exception"):
        self.__message = message

    def __str__(self):
        return self.__message

class InvalidMoveException(GameException):
    def __init__(self):
        super().__init__("Invalid move")

class GameOver(GameException):
    def __init__(self):
        super().__init__("Game Over.")