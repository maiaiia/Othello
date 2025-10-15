import pygame
from pygame.sprite import Sprite
import pygame.freetype

from src.constants import GUIConstants

class RegularText(Sprite):
    def __init__(self, text, center_position, font_size=30, text_color=GUIConstants.TEXT_COLOR, background_color=GUIConstants.BACKGROUND_COLOR):

        self.__font_size = font_size
        self.__text_color = text_color
        self.__background_color = background_color
        self.__center_position = center_position

        self.__text = RegularText.create_text_surface(text, font_size, text_color, background_color)
        self.__rectangle = self.__text.get_rect(center=center_position)
        super().__init__()

    @property
    def text(self):
        return self.__text

    @property
    def rectangle(self):
        return self.__rectangle

    def set_text(self, new_text):
        self.__text = RegularText.create_text_surface(new_text, self.__font_size, self.__text_color, self.__background_color)
        self.__rectangle = self.__text.get_rect(center=self.__center_position)

    @staticmethod
    def create_text_surface(text, font_size, text_color, background_color):
        font = pygame.freetype.SysFont("Courier", font_size, bold=True)
        surface, rectangle = font.render(text=text, fgcolor=text_color, bgcolor=background_color)
        return surface.convert_alpha()

    def draw_text_on_surface(self, surface):
        surface.blit(self.text, self.rectangle)

class ResponsiveText(Sprite):
    def __init__(self, center_position, text, font_size, text_color, background_color, action=None):
        self.__mouse_over = False
        default_text = RegularText(text, center_position, font_size, text_color, background_color)
        highlighted_text = RegularText(text, center_position, font_size*1.2, text_color, background_color)
        self.__outputs = { False:default_text, True:highlighted_text }
        self.__action = action

        super().__init__()

    @property
    def active_text(self):
        return self.__outputs[self.__mouse_over]

    def update_mouse_over(self, mouse_position, mouse_click):
        if self.active_text.rectangle.collidepoint(mouse_position):
            self.__mouse_over = True
            if mouse_click:
                return self.__action
        else:
            self.__mouse_over = False
        return None

    def draw_text_on_surface(self, surface):
        self.active_text.draw_text_on_surface(surface)

class Button(ResponsiveText):
    def __init__(self, center_position, text, action,font_size=30,text_color=GUIConstants.TEXT_COLOR,background_color=GUIConstants.BACKGROUND_COLOR):
        super().__init__(
            center_position=center_position,
            text=text,
            font_size=font_size,
            text_color=text_color,
            background_color=background_color,
            action=action
        )