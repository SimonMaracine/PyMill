from math import sqrt
import pygame
from src.display import WIDTH, HEIGHT
from src.piece import Piece
from src.node import Node


class Table:
    def __init__(self):
        self.width = HEIGHT - 40
        self.x = (WIDTH - self.width) // 2
        self.y = (HEIGHT - self.width) // 2
        self.DIV = self.width // 6
        self.nodes = [
            Node(self.x, self.y),
            Node(self.x + self.DIV * 3, self.y),
            Node(self.x + self.DIV * 6, self.y),  # line
            Node(self.x + self.DIV, self.y + self.DIV),
            Node(self.x + self.DIV * 3, self.y + self.DIV),
            Node(self.x + self.DIV * 5, self.y + self.DIV),  # line
            Node(self.x + self.DIV * 2, self.y + self.DIV * 2),
            Node(self.x + self.DIV * 3, self.y + self.DIV * 2),
            Node(self.x + self.DIV * 4, self.y + self.DIV * 2),  # line
            Node(self.x, self.y + self.DIV * 3),
            Node(self.x + self.DIV, self.y + self.DIV * 3),
            Node(self.x + self.DIV * 2, self.y + self.DIV * 3),  # line
            Node(self.x + self.DIV * 4, self.y + self.DIV * 3),
            Node(self.x + self.DIV * 5, self.y + self.DIV * 3),
            Node(self.x + self.DIV * 6, self.y + self.DIV * 3),  # line
            Node(self.x + self.DIV * 2, self.y + self.DIV * 4),
            Node(self.x + self.DIV * 3, self.y + self.DIV * 4),
            Node(self.x + self.DIV * 4, self.y + self.DIV * 4),  # line
            Node(self.x + self.DIV, self.y + self.DIV * 5),
            Node(self.x + self.DIV * 3, self.y + self.DIV * 5),
            Node(self.x + self.DIV * 5, self.y + self.DIV * 5),  # line
            Node(self.x, self.y + self.DIV * 6),
            Node(self.x + self.DIV * 3, self.y + self.DIV * 6),
            Node(self.x + self.DIV * 6, self.y + self.DIV * 6)  # line
        ]
        for node in self.nodes:  # correct the position of each node
            node.x += 1
            node.y += 1
        self.pieces = []

    def render(self, surface):
        # Drawing three rectangles...
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.width), 2)
        pygame.draw.rect(surface, (0, 0, 0), (self.x + self.DIV, self.y + self.DIV,
                                              self.width - self.DIV * 2, self.width - self.DIV * 2), 2)
        pygame.draw.rect(surface, (0, 0, 0), (self.x + self.DIV * 2, self.y + self.DIV * 2,
                                              self.width - self.DIV * 4, self.width - self.DIV * 4), 2)
        # ... and four middle lines.
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.DIV * 3, self.y),
                         (self.x + self.DIV * 3, self.y + self.DIV * 2), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x, self.y + self.DIV * 3),
                         (self.x + self.DIV * 2, self.y + self.DIV * 3), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.DIV * 3, self.y + self.DIV * 6),
                         (self.x + self.DIV * 3, self.y + self.DIV * 4), 2)
        pygame.draw.line(surface, (0, 0, 0), (self.x + self.DIV * 6, self.y + self.DIV * 3),
                         (self.x + self.DIV * 4, self.y + self.DIV * 3), 2)

        for node in self.nodes:
            node.render(surface)

        for piece in self.pieces:
            piece.render(surface)

    def update(self, mouse: tuple):
        mouse_x = mouse[0]
        mouse_y = mouse[1]
        for node in self.nodes:
            distance = sqrt(((mouse_x - node.x) ** 2 + (mouse_y - node.y) ** 2))
            if distance <= node.radius:
                node.highlight = True
            else:
                node.highlight = False

    def put_new_piece(self):
        for node in self.nodes:
            if node.highlight and not node.has_piece:
                self.pieces.append(Piece(node.x, node.y, (255, 255, 255)))
                node.has_piece = True
                break
