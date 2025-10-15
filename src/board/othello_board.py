from src.board.board import Board
from src.constants import BoardConstants

class OthelloBoard(Board):
    def __init__(self):
        super().__init__()
        self.__place_starting_pieces()

    def __place_starting_pieces(self):
        center_row_column = self.board_size // 2 - 1
        self.place_piece(center_row_column, center_row_column, BoardConstants.WHITE)
        self.place_piece(center_row_column+1, center_row_column+1, BoardConstants.WHITE)
        self.place_piece(center_row_column, center_row_column+1, BoardConstants.BLACK)
        self.place_piece(center_row_column+1, center_row_column, BoardConstants.BLACK)

    def reset_board(self):
        super().reset_board()
        self.__place_starting_pieces()

    """capture logic"""
    def get_final_position_to_capture(self, row: int, column: int, direction: [int, int], piece_to_add: BoardConstants.BLACK or BoardConstants.WHITE):
        row_offset, column_offset = direction
        next_row, next_column = row + row_offset, column + column_offset
        while ((0 <= next_row < self.board_size) and (0 <= next_column < self.board_size) and
               self.get_piece(next_row,next_column) == self.get_opposite_color(piece_to_add)):
            next_row += row_offset
            next_column += column_offset
        if ((0 <= next_row < self.board_size) and (0 <= next_column < self.board_size) and
                self.get_piece(next_row,next_column) == piece_to_add and
                (next_row != row + row_offset or next_column != column + column_offset)):
            return next_row, next_column
        return None

    def capture_diagonal(self, start_row: int, start_column: int, end_row: int, end_column: int, direction: [int, int]):
        row_offset, column_offset = direction
        current_row = start_row + row_offset
        current_column = start_column + column_offset

        while current_row != end_row or current_column != end_column:
            self.flip_piece(current_row, current_column)
            current_row += row_offset
            current_column += column_offset

    def capture_all(self, row: int, column: int, piece_type: BoardConstants.BLACK or BoardConstants.WHITE):
        for direction in BoardConstants.VALID_DIRECTIONS:
            final_position_to_replace = self.get_final_position_to_capture(row, column, direction, piece_type)
            if final_position_to_replace:
                end_row, end_column = final_position_to_replace
                self.capture_diagonal(row, column, end_row, end_column, direction)

    def move(self, row, column, piece_type):
        self.place_piece(row, column, piece_type)
        self.capture_all(row, column, piece_type)
