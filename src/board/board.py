from src.constants import BoardConstants

class Board:
    def __init__(self):
        self.__board_size = 8
        self.__board = [[BoardConstants.EMPTY_CELL for _ in range(self.__board_size)] for _ in range(self.__board_size)]
        self.__piece_count = {BoardConstants.WHITE : 0, BoardConstants.BLACK : 0}

    def reset_board(self):
        self.__board = [[BoardConstants.EMPTY_CELL for _ in range(self.__board_size)] for _ in range(self.__board_size)]
        self.__piece_count = {BoardConstants.BLACK: 0, BoardConstants.WHITE: 0}

    """getters"""
    @property
    def board_size(self):
        return self.__board_size
    @property
    def piece_count(self):
        return self.__piece_count

    def get_piece(self, row, column):
        return self.__board[row][column]

    @staticmethod
    def get_opposite_color(piece_type: BoardConstants.BLACK or BoardConstants.WHITE):
        return BoardConstants.EMPTY_CELL if piece_type == BoardConstants.EMPTY_CELL else\
            BoardConstants.BLACK if piece_type == BoardConstants.WHITE else BoardConstants.WHITE

    """crude operations"""
    def place_piece(self, row: int, column: int, piece_type):
        self.__board[row][column] = piece_type
        self.__piece_count[piece_type] += 1

    def remove_piece(self, row: int, column: int):
        self.__piece_count[self.get_piece(row, column)] -= 1
        self.__board[row][column] = BoardConstants.EMPTY_CELL

    def flip_piece(self, row: int, column: int):
        flipped_piece_type = self.get_opposite_color(self.get_piece(row, column))
        self.remove_piece(row, column)
        self.place_piece(row,column,flipped_piece_type)

    def get_piece_count(self, piece_type: BoardConstants.BLACK or BoardConstants.WHITE):
        return self.__piece_count[piece_type]
