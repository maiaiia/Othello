from texttable import Texttable
from src.board.othello_board import OthelloBoard
from src.constants import BoardConstants
from src.game.computer_strategy import ComputerStrategyEasy, ComputerStrategyMedium, ComputerStrategyHard, ComputerStrategyImpossible
from src.game.game import Game
from src.game.game_exceptions import GameOver
from src.game.move_validator import MoveValidator

import pyfiglet
from colorama import Fore, Style

class UI:
    def __init__(self, computer_strategy=None):
        self._board = OthelloBoard()
        self._game = Game(self._board)
        self._computer_strategy = computer_strategy

    def set_computer_strategy(self, computer_strategy):
        self._computer_strategy = computer_strategy(self._game)

class CUI(UI):
    def __init__(self, computer_strategy=None):
        super().__init__(computer_strategy)
        self.__first_game = True

    """Display stuff"""
    def print_board(self, valid_moves=[]):
        board = Texttable()
        header = [' '] + [i for i in range(self._board.board_size)]
        board.add_row(header)
        row_number = 0
        for row in range(self._board.board_size):
            new_row = [row_number]
            row_number += 1
            for column in range(self._board.board_size):
                if (row, column) in valid_moves:
                    new_row.append('*')
                else:
                    new_row.append(self._board.get_piece(row,column))
            board.add_row(new_row)
        print(board.draw())

    @staticmethod
    def print_panel():
        # basic / epic / fender / shimrod / small
        welcome_message = pyfiglet.figlet_format("       Welcome to\nReversi / Othello", font="small")
        print(welcome_message)

    def print_human_board(self):
        print(Fore.CYAN)
        self.print_board()
        self.print_score()
        print(Style.RESET_ALL)

    def print_computer_board(self, valid_moves=[]):
        print(Fore.GREEN)
        self.print_board(valid_moves)
        self.print_score()
        print(Style.RESET_ALL)

    def print_final_board(self):
        print(Fore.GREEN)
        print(Style.BRIGHT)
        self.print_board()
        print(Style.RESET_ALL)

    def print_winner(self):
        winner = self._game.get_winner()
        if winner == BoardConstants.BLACK:
            print("Black Won!")
        elif winner == BoardConstants.WHITE:
            print("White Won!")
        else:
            print("It's a Draw!")

    def print_score(self):
        score_values = self._game.get_score()
        score_to_display = ""
        for score_value in score_values.items():
            piece_type, piece_count = score_value
            score_to_display += ("B" if piece_type == BoardConstants.BLACK else "W")
            score_to_display += " : "
            score_to_display += str(piece_count) + " - "
        print(score_to_display.strip(" - "))

    """User input methods"""
    def select_computer_strategy(self):
        computer_strategy = self.get_difficulty()
        super().set_computer_strategy(computer_strategy)

    @staticmethod
    def get_difficulty():
        difficulties = {"easy": ComputerStrategyEasy,
                        "medium": ComputerStrategyMedium,
                        "hard": ComputerStrategyHard,
                        "impossible": ComputerStrategyImpossible
                        }

        user_choice = input("Enter a difficulty level (easy / medium / hard / impossible): ").strip().lower()
        while user_choice not in difficulties.keys():
            print("Invalid option.")
            user_choice = input("Enter a difficulty level (easy / medium / hard / impossible): ").strip().lower()
        return difficulties[user_choice]

    @staticmethod
    def get_first_player():
        human_turn = input("Would you like to go first (white pieces)? y/n ").strip().lower()
        while human_turn not in ["y", "n"]:
            print("Invalid option. ")
            human_turn = input("Would you like to go first? y/n ").strip().lower()
        return human_turn == 'y'

    @staticmethod
    def get_human_player_move():
        try:
            row = int(input("Enter row: "))
            column = int(input("Enter column: "))
        except ValueError:
            raise ValueError("Row and column must be integers")
        return row, column

    """Start game"""
    def start(self):
        if self.__first_game:
            self.print_panel()
            self.__first_game = False
        self.select_computer_strategy()
        human_turn = self.get_first_player()
        print("Board initialized successfully. ")
        while True:
            try:
                valid_moves = MoveValidator.get_valid_moves(self._game.board, self._game.turn)
                if not valid_moves:
                    self._game.increase_pass_count()
                    print("Pass!")
                    human_turn = not human_turn
                    continue

                if human_turn:
                    self.print_computer_board(valid_moves)
                    row, column = self.get_human_player_move()
                    self._game.move(row, column)
                else:
                    self.print_human_board()
                    row, column = self._computer_strategy.get_move(valid_moves)
                    self._game.move(row, column)
                human_turn = not human_turn
            except GameOver:
                break
            except Exception as error:
                print(error)
                continue

        self.print_final_board()
        self.print_winner()
        self.print_score()

        play_again = input("Play again? y/n ")
        if play_again.lower().strip() == 'y':
            self._game.reset_game()
            self.start()

if __name__ == "__main__":
    ui = CUI()
    ui.start()