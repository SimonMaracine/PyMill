from math import sqrt
import pygame


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 29
        self.highlight = False
        self.highlight_color = (16, 200, 15)
        self.piece = None

    def render(self, surface):
        pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), 11)
        if self.highlight:
            pygame.draw.ellipse(surface, self.highlight_color,
                                (self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2), 3)

    def update(self, mouse_x, mouse_y):
        distance = sqrt(((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2))
        if distance <= self.radius:
            self.highlight = True
        else:
            self.highlight = False

    def add_piece(self, piece):
        self.piece = piece

    def take_piece(self):
        self.piece = None
