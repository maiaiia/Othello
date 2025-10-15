from src.UI.ui import UI
import pygame
import pygame.freetype
import time

from src.constants import GUIConstants, BoardConstants, GameState
from src.game.computer_strategy import ComputerStrategyEasy, ComputerStrategyMedium, ComputerStrategyHard, \
    ComputerStrategyImpossible
from src.game.game_exceptions import GameOver
from src.game.move_validator import MoveValidator

from src.UI.gui_elements import Button, RegularText

class GUI(UI):
    def __init__(self, computer_strategy=None):
        super().__init__(computer_strategy)
        self.__window = pygame.display.set_mode((GUIConstants.WINDOW_WIDTH, GUIConstants.WINDOW_HEIGHT))
        self.configure_window()

        self.__human_turn = False

    def configure_window(self):
        pygame.display.set_caption("Reversi / Othello")
        self.__window.fill(GUIConstants.BACKGROUND_COLOR)
        pygame.display.update()

    def draw_board(self):
        for row in range(BoardConstants.BOARD_SIZE):
            for column in range(BoardConstants.BOARD_SIZE):
                if (row + column) % 2: #dark
                    pygame.draw.rect(self.__window, GUIConstants.DARK_CELL_COLOR,
                                     (row * GUIConstants.CELL_SIZE, column * GUIConstants.CELL_SIZE, GUIConstants.CELL_SIZE, GUIConstants.CELL_SIZE))
                else:
                    pygame.draw.rect(self.__window, GUIConstants.LIGHT_CELL_COLOR,
                                     (row * GUIConstants.CELL_SIZE, column * GUIConstants.CELL_SIZE, GUIConstants.CELL_SIZE, GUIConstants.CELL_SIZE))

    def draw_piece(self, row, column, piece_color):
        piece_radius = GUIConstants.CELL_SIZE // 2 - GUIConstants.PIECE_PADDING
        display_row = GUIConstants.CELL_SIZE * row + GUIConstants.CELL_SIZE // 2
        display_column = GUIConstants.CELL_SIZE * column + GUIConstants.CELL_SIZE // 2
        if piece_color == BoardConstants.BLACK:
            pygame.draw.circle(self.__window, GUIConstants.DARK_PIECE_OUTLINE, (display_column, display_row), piece_radius + GUIConstants.PIECE_OUTLINE)
            pygame.draw.circle(self.__window, GUIConstants.DARK_PIECE_COLOR, (display_column, display_row), piece_radius)
        else:
            pygame.draw.circle(self.__window, GUIConstants.LIGHT_PIECE_OUTLINE, (display_column, display_row), piece_radius + GUIConstants.PIECE_OUTLINE)
            pygame.draw.circle(self.__window, GUIConstants.LIGHT_PIECE_COLOR, (display_column, display_row), piece_radius)

    def draw_all_pieces(self):
        for row in range(self._board.board_size):
            for column in range(self._board.board_size):
                piece_type = self._board.get_piece(row, column)
                if piece_type != BoardConstants.EMPTY_CELL:
                    self.draw_piece(row, column, piece_type)

    def update_game_display(self):
        self.draw_all_pieces()
        self.update_score()
        pygame.display.update()

    def update_score(self):
        self.initialize_score_board()
        score = self._game.get_score()
        score_white = RegularText(
            text="White: " + str(score[BoardConstants.WHITE]),
            center_position=(GUIConstants.BOARD_LENGTH+200, 200)
        )
        score_black = RegularText(
            text="Black: " + str(score[BoardConstants.BLACK]),
            center_position=(GUIConstants.BOARD_LENGTH+200, 250)
        )
        score_white.draw_text_on_surface(self.__window)
        score_black.draw_text_on_surface(self.__window)

    def initialize_othello_board(self):
        self.draw_board()
        self.update_game_display()
        pygame.display.update()

    def initialize_score_board(self):
        self.__window.fill(GUIConstants.BACKGROUND_COLOR, (GUIConstants.BOARD_LENGTH, 0, GUIConstants.WINDOW_WIDTH, GUIConstants.WINDOW_HEIGHT))
        scoreboard_title=RegularText(
            text="Scoreboard",
            center_position=(GUIConstants.BOARD_LENGTH+200,100),
            font_size=50
        )
        scoreboard_title.draw_text_on_surface(self.__window)


    def set_human_turn(self, piece_color):
        self.__human_turn = (True if piece_color == BoardConstants.WHITE else False)


    @staticmethod
    def get_valid_move_button(move):
        row, column = move
        center_row = row * GUIConstants.CELL_SIZE + GUIConstants.CELL_SIZE // 2
        center_column = column * GUIConstants.CELL_SIZE + GUIConstants.CELL_SIZE // 2

        return Button(
            center_position=(center_column,center_row),
            text="*",
            background_color=GUIConstants.HIGHLIGHT_COLOR,
            font_size=50,
            action=(row,column),
            text_color=GUIConstants.HIGHLIGHT_COLOR
        )

    def run_title_screen(self):
        play_button = Button(
            center_position=(GUIConstants.WINDOW_WIDTH // 2, GUIConstants.WINDOW_HEIGHT // 2),
            text="play",
            font_size=40,
            action=GameState.SETUP_SCREEN
        )
        quit_button = Button(
            center_position=(GUIConstants.WINDOW_WIDTH // 2, GUIConstants.WINDOW_HEIGHT // 2 + 100),
            text="exit",
            font_size=40,
            action=GameState.QUIT
        )
        game_title = RegularText(
            center_position=(GUIConstants.WINDOW_WIDTH // 2, GUIConstants.WINDOW_HEIGHT // 2 - 200),
            text="Reversi / Othello",
            font_size=60
        )
        text_elements = [game_title]
        buttons = [play_button, quit_button]

        while True:
            mouse_click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_click = True
            self.__window.fill(GUIConstants.BACKGROUND_COLOR)

            for text_element in text_elements:
                text_element.draw_text_on_surface(self.__window)

            for button in buttons:
                ui_action = button.update_mouse_over(pygame.mouse.get_pos(), mouse_click)
                if ui_action:
                    return ui_action
                button.draw_text_on_surface(self.__window)

            pygame.display.update()

    def run_setup_screen(self):
        play_button = Button(
            center_position=(GUIConstants.WINDOW_WIDTH-100, GUIConstants.WINDOW_HEIGHT-100),
            text="play",
            action=GameState.GAME_SCREEN
        )
        back_button = Button(
            center_position=(100,GUIConstants.WINDOW_HEIGHT-100),
            text="back",
            action=GameState.TITLE_SCREEN
        )
        difficulty_easy_button = Button(
            center_position=(300, GUIConstants.WINDOW_HEIGHT // 2-100),
            text="easy",
            action=ComputerStrategyEasy
        )
        difficulty_medium_button = Button(
            center_position=(300, GUIConstants.WINDOW_HEIGHT // 2-50),
            text="medium",
            action=ComputerStrategyMedium
        )
        difficulty_hard_button = Button(
            center_position=(300, GUIConstants.WINDOW_HEIGHT // 2),
            text="hard",
            action=ComputerStrategyHard
        )
        difficulty_impossible_button = Button(
            center_position=(300, GUIConstants.WINDOW_HEIGHT // 2+50),
            text="impossible",
            action=ComputerStrategyImpossible
        )
        user_color_white_button = Button(
            center_position=(GUIConstants.WINDOW_WIDTH-300, GUIConstants.WINDOW_HEIGHT // 2-75),
            text="white",
            action=BoardConstants.WHITE
        )
        user_color_black_button = Button(
            center_position=(GUIConstants.WINDOW_WIDTH - 300, GUIConstants.WINDOW_HEIGHT // 2+25),
            text="black",
            action=BoardConstants.BLACK
        )
        difficulty_message=RegularText(
            text="Choose level difficulty",
            center_position=(300, GUIConstants.WINDOW_HEIGHT // 2-200)
        )
        user_color_message=RegularText(
            text="Choose piece color",
            center_position=(GUIConstants.WINDOW_WIDTH - 300, GUIConstants.WINDOW_HEIGHT // 2-200)
        )
        selected_difficulty=RegularText(
            text="Difficulty: Easy",
            center_position=(300, GUIConstants.WINDOW_HEIGHT-200)
        )
        selected_color=RegularText(
            text="Piece Color: White",
            center_position=(GUIConstants.WINDOW_WIDTH-300, GUIConstants.WINDOW_HEIGHT-200)
        )

        text_elements = [difficulty_message, user_color_message, selected_difficulty, selected_color]
        game_state_buttons = [play_button, back_button]
        difficulty_buttons = [difficulty_easy_button, difficulty_medium_button, difficulty_hard_button, difficulty_impossible_button]
        user_color_buttons = [user_color_white_button, user_color_black_button]

        piece_colors={BoardConstants.BLACK:"Black", BoardConstants.WHITE:"White"}
        difficulties={ComputerStrategyEasy:"Easy", ComputerStrategyMedium:"Medium", ComputerStrategyHard:"Hard", ComputerStrategyImpossible:"Impossible"}

        self.set_computer_strategy(ComputerStrategyEasy)
        self.__human_turn = True

        while True:
            mouse_click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_click = True
            self.__window.fill(GUIConstants.BACKGROUND_COLOR)

            for text_element in text_elements:
                text_element.draw_text_on_surface(self.__window)

            for button in game_state_buttons:
                ui_action = button.update_mouse_over(pygame.mouse.get_pos(), mouse_click)
                if ui_action:
                    return ui_action
                button.draw_text_on_surface(self.__window)

            for button in difficulty_buttons:
                difficulty = button.update_mouse_over(pygame.mouse.get_pos(), mouse_click)
                if difficulty:
                    self.set_computer_strategy(difficulty)
                    selected_difficulty.set_text("Difficulty: "+difficulties[difficulty])
                button.draw_text_on_surface(self.__window)

            for button in user_color_buttons:
                piece_color = button.update_mouse_over(pygame.mouse.get_pos(), mouse_click)
                if piece_color:
                    self.set_human_turn(piece_color)
                    selected_color.set_text("Piece Color: " + piece_colors[piece_color])
                button.draw_text_on_surface(self.__window)

            pygame.display.update()

    def clear_button_area(self):
        pygame.draw.rect(self.__window, GUIConstants.BACKGROUND_COLOR, (800, 500, 1200, 800))

    def run_game(self):
        self._game.reset_game()
        self.__window.fill(GUIConstants.BACKGROUND_COLOR)
        self.initialize_othello_board()
        self.initialize_score_board()
        self.update_game_display()

        valid_moves = MoveValidator.get_valid_moves(self._game.board, self._game.turn)
        valid_move_buttons = [self.get_valid_move_button(valid_move) for valid_move in valid_moves]
        while True:
            try:
                mouse_click = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return GameState.QUIT
                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        mouse_click = True

                if not valid_moves:
                    self._game.increase_pass_count()
                    self.__human_turn = not self.__human_turn
                    valid_moves = MoveValidator.get_valid_moves(self._game.board, self._game.turn)
                    valid_move_buttons = [self.get_valid_move_button(valid_move) for valid_move in valid_moves]

                elif not self.__human_turn:
                    time.sleep(0.2)
                    row, column = self._computer_strategy.get_move(valid_moves)
                    self._game.move(row, column)
                    self.__human_turn = not self.__human_turn
                    valid_moves = MoveValidator.get_valid_moves(self._game.board, self._game.turn)
                    valid_move_buttons = [self.get_valid_move_button(valid_move) for valid_move in valid_moves]

                if self.__human_turn:
                    for button in valid_move_buttons:
                        ui_action = button.update_mouse_over(pygame.mouse.get_pos(), mouse_click)
                        if ui_action:
                            self._game.move(*ui_action)
                            valid_moves=MoveValidator.get_valid_moves(self._game.board, self._game.turn)
                            self.__human_turn = not self.__human_turn
                            self.draw_board()
                            break
                        button.draw_text_on_surface(self.__window)
                self.update_game_display()
            except GameOver:
                break

        winner=self._game.get_winner()
        if winner == -1:
            winner_message_text = "Draw!"
        else:
            winner_message_text= ("White" if winner == BoardConstants.WHITE else "Black") + " won!"
        winner_message = RegularText(
            text=winner_message_text,
            center_position=(GUIConstants.BOARD_LENGTH+200, 400)
        )
        winner_message.draw_text_on_surface(self.__window)
        play_again = Button(
            text="play again",
            center_position=(GUIConstants.BOARD_LENGTH+200, 550),
            action=GameState.SETUP_SCREEN
        )
        back_to_menu = Button(
            text="return to menu",
            center_position=(GUIConstants.BOARD_LENGTH+200, 600),
            action=GameState.TITLE_SCREEN
        )
        exit_game = Button(
            text="exit",
            center_position=(GUIConstants.BOARD_LENGTH+200, 650),
            action=GameState.QUIT
        )
        game_state_buttons = [play_again, back_to_menu, exit_game]
        while True:
            mouse_click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return GameState.QUIT
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_click = True
            self.clear_button_area()
            for button in game_state_buttons:
                ui_action = button.update_mouse_over(pygame.mouse.get_pos(), mouse_click)
                if ui_action:
                    return ui_action
                button.draw_text_on_surface(self.__window)
            pygame.display.update()

    def start(self):
        pygame.init()
        game_state = GameState.TITLE_SCREEN

        while True:
            if game_state == GameState.TITLE_SCREEN:
                game_state = self.run_title_screen()
            elif game_state == GameState.SETUP_SCREEN:
                game_state = self.run_setup_screen()
            elif game_state == GameState.GAME_SCREEN:
                game_state = self.run_game()
            elif game_state == GameState.QUIT:
                pygame.quit()
                return


def main():
    ui = GUI()
    ui.start()

if __name__ == "__main__":
    main()