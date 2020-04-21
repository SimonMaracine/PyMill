from math import sqrt
import pygame


class Node:
    """Class representing a node object used by the Board."""

    DEFAULT_RADIUS = 34
    DEFAULT_DOT_RADIUS = 16

    radius = DEFAULT_RADIUS
    dot_radius = DEFAULT_DOT_RADIUS
    highlight_color = (200, 190, 210)

    def __init__(self, x: int, y: int, search: tuple, id_: int):
        self.x = x
        self.y = y
        self.search = search  # represents its neighbors
        self.id = id_
        self.highlight = False
        self.color = (0, 0, 0)
        self.piece = None
        self.remove_thingy = False

    def __repr__(self):
        return f"{self.id}, {self.piece}"

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), Node.dot_radius)
        if self.highlight:
            pygame.draw.ellipse(surface, Node.highlight_color,
                                (self.x - Node.radius, self.y - Node.radius, Node.radius * 2, Node.radius * 2), 4)

    def update(self, mouse_x: int, mouse_y: int, must_remove_piece: bool):
        distance = sqrt(((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2))
        if distance <= Node.radius:
            self.highlight = True
        else:
            self.highlight = False

        if must_remove_piece:
            self.remove_thingy = True
        else:
            self.remove_thingy = False

    def render_remove_thingy(self, surface: pygame.Surface):
        if self.highlight and self.remove_thingy:
            pygame.draw.line(surface, Node.highlight_color, (self.x - Node.radius // 2, self.y - Node.radius // 2),
                             (self.x + Node.radius // 2, self.y + Node.radius // 2), 4)
            pygame.draw.line(surface, Node.highlight_color, (self.x + Node.radius // 2, self.y - Node.radius // 2),
                             (self.x - Node.radius // 2, self.y + Node.radius // 2), 4)

    def add_piece(self, piece):
        assert piece is not None

        self.piece = piece
        self.piece.x = self.x
        self.piece.y = self.y

    def take_piece(self):
        assert self.piece is not None

        self.piece = None

    def change_color(self, color: tuple):
        self.color = color

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y
        if self.piece is not None:
            self.piece.x = x
            self.piece.y = y

    def search_neighbors(self, nodes: tuple) -> tuple:
        if self.id == 0:
            return nodes[1], nodes[9]
        elif self.id == 1:
            return nodes[0], nodes[2], nodes[4]
        elif self.id == 2:
            return nodes[1], nodes[14]
        elif self.id == 3:
            return nodes[4], nodes[10]
        elif self.id == 4:
            return nodes[1], nodes[3], nodes[5], nodes[7]
        elif self.id == 5:
            return nodes[4], nodes[13]
        elif self.id == 6:
            return nodes[7], nodes[11]
        elif self.id == 7:
            return nodes[4], nodes[6], nodes[8]
        elif self.id == 8:
            return nodes[7], nodes[12]
        elif self.id == 9:
            return nodes[0], nodes[10], nodes[21]
        elif self.id == 10:
            return nodes[3], nodes[9], nodes[11], nodes[18]
        elif self.id == 11:
            return nodes[6], nodes[10], nodes[15]
        elif self.id == 12:
            return nodes[8], nodes[13], nodes[17]
        elif self.id == 13:
            return nodes[5], nodes[12], nodes[14], nodes[20]
        elif self.id == 14:
            return nodes[2], nodes[13], nodes[23]
        elif self.id == 15:
            return nodes[11], nodes[16]
        elif self.id == 16:
            return nodes[15], nodes[17], nodes[19]
        elif self.id == 17:
            return nodes[12], nodes[16]
        elif self.id == 18:
            return nodes[10], nodes[19]
        elif self.id == 19:
            return nodes[16], nodes[18], nodes[20], nodes[22]
        elif self.id == 20:
            return nodes[13], nodes[19]
        elif self.id == 21:
            return nodes[9], nodes[22]
        elif self.id == 22:
            return nodes[19], nodes[21], nodes[23]
        else:
            return nodes[14], nodes[22]
