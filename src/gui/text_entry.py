import pygame
from src.fonts import text_entry_font


class TextEntry:
    def __init__(self, x: int, y: int, width: int):
        self.x = x
        self.y = y
        self.width = width
        self.text = []

    def render(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, 40), 4)
        text = text_entry_font.render(self.get_text()[:-1], True, (0, 0, 0))
        surface.blit(text, (self.x + 6, self.y + 6))

    def update(self):
        pass

    def get_text(self) -> str:
        return "".join(self.text)
