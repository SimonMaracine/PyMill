import pygame


class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 23
        self.picked_up = False

    def render(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
