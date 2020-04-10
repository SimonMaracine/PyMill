import pygame
import pygame.gfxdraw
from src.constants import *


class Piece:
    """Class representing a piece object used by the Board."""

    DEFAULT_RADIUS = 28

    radius = DEFAULT_RADIUS

    def __init__(self, x: int, y: int, color: tuple):
        self.x = x
        self.y = y
        self.color = color
        self.picked_up = False

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), Piece.radius)
        if self.color == WHITE:
            pygame.gfxdraw.circle(surface, self.x, self.y, Piece.radius, (0, 0, 0))
        else:
            pygame.gfxdraw.circle(surface, self.x, self.y, Piece.radius, WHITE)

    def update(self, mouse_x: int, mouse_y: int):
        if self.picked_up:
            self.x = mouse_x
            self.y = mouse_y

    def pick_up(self, turn: int) -> bool:
        if (turn == PLAYER1 and self.color == WHITE) or (turn == PLAYER2 and self.color == BLACK):
            self.picked_up = True
            return True
        else:
            return False

    def release(self, node):
        self.picked_up = False
        self.x = node.x
        self.y = node.y
