import copy
from random import randint

from src.board.othello_board import OthelloBoard
from src.constants import BoardConstants
from src.game.game import Game
from src.game.move_validator import MoveValidator

class ComputerStrategy:
    def __init__(self, game: Game):
        self._game = game

    def get_move(self, valid_moves):
        pass

class ComputerStrategyEasy(ComputerStrategy):
    def get_move(self, valid_moves: list[int,int]):
        if not valid_moves:
            return None
        return valid_moves[randint(0, len(valid_moves) - 1)]

class ComputerStrategyMiniMax(ComputerStrategy):
    __MAX_POINTS = 65  # board has 64 cells

    def get_move(self, valid_moves: list[int, int]):
        if not valid_moves:
            return None
        best_score, best_move = ComputerStrategyHard._get_best_score_and_move_minimax(self._game.board, 3, self._game.turn)
        return best_move

    @staticmethod
    def _get_best_score_and_move_minimax(board: OthelloBoard, depth:int, turn: BoardConstants.BLACK or BoardConstants.WHITE,
                                         best_score_white=-__MAX_POINTS, best_score_black=__MAX_POINTS) -> [int, [int, int]]:

        valid_moves = MoveValidator.get_valid_moves(board, turn)
        if not valid_moves or not depth:
            return ComputerStrategyMiniMax.__evaluate_board_state(board), None

        if turn == BoardConstants.WHITE:  # maximizing player
            best_score = - ComputerStrategyMiniMax.__MAX_POINTS
            best_move = None

            for move in valid_moves:
                move_row, move_column = move

                new_move_board = copy.deepcopy(board)
                new_move_board.move(move_row, move_column, turn)
                subtree_best_score, subtree_best_move = ComputerStrategyMiniMax._get_best_score_and_move_minimax(new_move_board, depth - 1,
                                                                                                                 BoardConstants.BLACK,
                                                                                                                 best_score_white, best_score_black)
                if subtree_best_score > best_score:
                    best_score = subtree_best_score
                    best_move = move
                best_score_white = max(best_score, best_score_white)
                if best_score_white >= best_score_black:
                    break
        else:
            best_score = ComputerStrategyMiniMax.__MAX_POINTS
            best_move = None

            for move in valid_moves:
                move_row, move_column = move

                new_move_board = copy.deepcopy(board)
                new_move_board.move(move_row, move_column, turn)
                subtree_best_score, subtree_best_move = ComputerStrategyMiniMax._get_best_score_and_move_minimax(new_move_board, depth - 1,
                                                                                                                 BoardConstants.WHITE,
                                                                                                                 best_score_white, best_score_black)
                if subtree_best_score < best_score:
                    best_score = subtree_best_score
                    best_move = move
                best_score_black = min(best_score, best_score_black)
                if best_score_white >= best_score_black:
                    break

        return best_score, best_move

    @staticmethod
    def __evaluate_board_state(board: OthelloBoard):
        return board.get_piece_count(BoardConstants.WHITE) - board.get_piece_count(BoardConstants.BLACK)

class ComputerStrategyMedium(ComputerStrategyMiniMax):
    def get_move(self, valid_moves: list[int, int]):
        if not valid_moves:
            return None
        best_score, best_move = self._get_best_score_and_move_minimax(self._game.board, 1, self._game.turn)
        return best_move

class ComputerStrategyHard(ComputerStrategyMiniMax):
    def get_move(self, valid_moves: list[int,int]):
        if not valid_moves:
            return None
        best_score, best_move = self._get_best_score_and_move_minimax(self._game.board, 3, self._game.turn)
        return best_move

class ComputerStrategyImpossible(ComputerStrategyMiniMax):
    def get_move(self, valid_moves):
        if not valid_moves:
            return None
        best_score, best_move = self._get_best_score_and_move_minimax(self._game.board, 5, self._game.turn)
        return best_move