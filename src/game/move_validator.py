from src.constants import BoardConstants
from src.board.othello_board import OthelloBoard
from src.board.board_exceptions import OutOfBoundsException, PositionUnavailableException
from src.game.game_exceptions import InvalidMoveException

class MoveValidator:
    @staticmethod
    def validate_move(board: OthelloBoard, row: int, column: int, piece_type: BoardConstants.BLACK or BoardConstants.WHITE):
        if not (0 <= row < board.board_size) or not (0 <= column < board.board_size):
            raise OutOfBoundsException
        if board.get_piece(row, column) != BoardConstants.EMPTY_CELL:
            raise PositionUnavailableException
        for direction in BoardConstants.VALID_DIRECTIONS:
            final_position_to_capture = board.get_final_position_to_capture(row, column, direction, piece_type)
            if final_position_to_capture:
                return True
        raise InvalidMoveException

    @staticmethod
    def get_valid_moves(board: OthelloBoard, turn: BoardConstants.BLACK or BoardConstants.WHITE):
        valid_moves = []
        for row in range(board.board_size):
            for column in range(board.board_size):
                try:
                    MoveValidator.validate_move(board, row, column, turn)
                    valid_moves.append((row, column))
                except InvalidMoveException:
                    continue
                except PositionUnavailableException:
                    continue
        return valid_moves