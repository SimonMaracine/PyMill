from math import sqrt
import pygame


class Node:
    """Class representing a node object used by the Board."""

    DEFAULT_RADIUS = 34
    DEFAULT_DOT_RADIUS = 16

    radius = DEFAULT_RADIUS
    dot_radius = DEFAULT_DOT_RADIUS

    def __init__(self, x: int, y: int, search: tuple, id_: int):
        self.x = x
        self.y = y
        self.search = search  # represents its neighbors
        self.id = id_
        self.highlight = False
        self.highlight_color = (180, 170, 190)
        self.color = (0, 0, 0)
        self.piece = None
        self.remove_thingy = False

    def __repr__(self):
        return "[{}, {}; {}]".format(self.x // 90, self.y // 90, True if self.piece else False)

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), Node.dot_radius)
        if self.highlight:
            pygame.draw.ellipse(surface, self.highlight_color,
                                (self.x - Node.radius, self.y - Node.radius, Node.radius * 2, Node.radius * 2), 3)

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
            pygame.draw.line(surface, self.highlight_color, (self.x - Node.radius // 2, self.y - Node.radius // 2),
                             (self.x + Node.radius // 2, self.y + Node.radius // 2), 3)
            pygame.draw.line(surface, self.highlight_color, (self.x + Node.radius // 2, self.y - Node.radius // 2),
                             (self.x - Node.radius // 2, self.y + Node.radius // 2), 3)

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

    def search_neighbors(self, nodes: tuple, div: int) -> tuple:
        search_north, search_south, search_east, search_west = self.search
        neighbor_nodes = []
        x = self.x
        y = self.y

        for i in range(1, 4):
            for node in nodes:
                if search_east:
                    if (x + div * i, y) == (node.x, node.y):
                        # print("Found node on the E. Distance = {} DIVs".format(i))
                        neighbor_nodes.append(node)
                        search_east = 0
                if search_south:
                    if (x, y + div * i) == (node.x, node.y):
                        # print("Found node on the S. Distance = {} DIVs".format(i))
                        neighbor_nodes.append(node)
                        search_south = 0

        x = self.x
        y = self.y

        for i in range(1, 4):
            for node in nodes:
                if search_west:
                    if (x - div * i, y) == (node.x, node.y):
                        # print("Found node on the W. Distance = {} DIVs".format(i))
                        neighbor_nodes.append(node)
                        search_west = 0
                if search_north:
                    if (x, y - div * i) == (node.x, node.y):
                        # print("Found node on the N. Distance = {} DIVs".format(i))
                        neighbor_nodes.append(node)
                        search_north = 0

        return tuple(neighbor_nodes)
