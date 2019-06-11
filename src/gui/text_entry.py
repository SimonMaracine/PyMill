import pygame


class TextEntry:
    def __init__(self, x: int, y: int, width: int):
        self.x = x
        self.y = y
        self.width = width
        self.text = []

    def render(self, surface):
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, 40), 4)

    def get_text(self) -> str:
        return "".join(self.text)
