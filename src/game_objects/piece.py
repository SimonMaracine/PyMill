import pygame
from src.constants import *


class Piece:
    radius = 28

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.picked_up = False

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def update(self, mouse_x, mouse_y):
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
