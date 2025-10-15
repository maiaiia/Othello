from src.board.othello_board import OthelloBoard
from src.game.move_validator import MoveValidator
from src.constants import BoardConstants
from src.game.game_exceptions import GameOver

class Game:
    def __init__(self, board: OthelloBoard):
        self.__board = board
        self.__pass_count = 0
        self.__turn=BoardConstants.WHITE

    @property
    def turn(self):
        return self.__turn

    @property
    def board(self):
        return self.__board

    def get_score(self):
        return self.__board.piece_count

    def get_score_difference(self):
        return self.__board.get_piece_count(BoardConstants.WHITE) - self.__board.get_piece_count(BoardConstants.BLACK)

    def increase_pass_count(self):
        self.__pass_count += 1
        self.__turn = self.__board.get_opposite_color(self.__turn)
        if self.__pass_count == 2:
            raise GameOver

    def reset_pass_count(self):
        self.__pass_count = 0

    def move(self, row, column):
        MoveValidator.validate_move(self.__board, row, column, self.turn)
        self.__board.move(row, column, self.turn)
        self.__turn = self.__board.get_opposite_color(self.__turn)
        self.reset_pass_count()

    def get_winner(self):
        score = self.get_score_difference()
        if not score:
            return -1
        return BoardConstants.WHITE if score > 0 else BoardConstants.BLACK

    def reset_game(self):
        self.__board.reset_board()
        self.reset_pass_count()
        self.__turn=BoardConstants.WHITE