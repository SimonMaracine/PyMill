import pygame
from src.fonts import text_entry_font
from src.constants import *


class TextEntry:
    def __init__(self, x: int, y: int, width: int, max_chars: int):
        self.x = x
        self.y = y
        self.width = width
        self.max_chars = max_chars
        self.height = 40
        self.text_array = []
        self.text = None
        self.font = text_entry_font
        self.focus = False
        self.locked = False
        self.color = (0, 0, 0)
        self.caret = Caret(self.x + 7, self.y + 6, 3, 28, self.font)
        self.focus_color = (255, 255, 255)
        self.surface = pygame.Surface((self.width - 8, self.height - 8))
        self.surface.set_clip(None)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 4)
        if self.focus:
            pygame.draw.rect(surface, self.focus_color, (self.x + 2, self.y + 2, self.width - 3, self.height - 3), 3)
        self.text = self.font.render(self.get_text(), True, self.color)

        self.surface.fill(BACKGROUND_COLOR)
        self.surface.blit(self.text, (4, 4))
        surface.blit(self.surface, (self.x + 4, self.y + 4))

        self.caret.render(surface)

    def update(self):
        if self.locked:
            self.color = (60, 60, 60)
        else:
            self.color = (0, 0, 0)

        if self.focus and not self.locked:
            self.caret.update()
        else:
            self.caret.visible = False

        if self.text:
            if self.x + self.text.get_width() + 7 >= self.x + self.width - 7:
                self.caret.visible = False

    def hovered(self, mouse: tuple) -> bool:
        if self.x + self.width >= mouse[0] >= self.x:
            if self.y + self.height >= mouse[1] >= self.y:
                return True
        return False

    def pressed(self, mouse: tuple, mouse_pressed: tuple) -> bool:
        if self.locked:
            return False
        if mouse_pressed[0]:
            if self.hovered(mouse):
                return True
        return False

    def insert_character(self, character: str):
        if self.focus and not self.locked:
            if len(self.text_array) < self.max_chars:
                self.text_array.append(character)
                # print(self.text_array)
                self.caret.move(1, character)

    def backspace(self):
        if self.focus and not self.locked:
            if self.text_array:
                character = self.text_array.pop()
                # print(self.text_array)
                self.caret.move(-1, character)

    def insert_text(self, text: str):
        self.text_array.clear()
        self.caret.x = self.x + 7
        if len(self.text_array) < self.max_chars:
            for ch in text:
                self.text_array.append(ch)
                self.caret.move(1, ch)

    def set_focus(self, focus: bool):
        self.focus = focus

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def get_text(self) -> str:
        return "".join(self.text_array)


class Caret:
    def __init__(self, x: int, y: int, width: int, height: int, font: pygame.font.Font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.color = (0, 0, 0)
        self.updt_count = 0
        self.visible = False

    def render(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        self.blink()

    def blink(self):
        self.updt_count += 1
        if self.updt_count % 25 == 0:
            self.visible = not self.visible
        if self.updt_count > 10000:
            self.updt_count = 0

    def move(self, direction: int, character: str):
        if direction < 0:
            if character == "j" or character == "f":
                self.x -= self.font.size(character)[0] - 1
            else:
                self.x -= self.font.size(character)[0]
        elif direction > 0:
            if character == "j" or character == "f":
                self.x += self.font.size(character)[0] - 1
            else:
                self.x += self.font.size(character)[0]
