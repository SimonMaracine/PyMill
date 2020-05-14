import tkinter as tk
from math import sqrt


class Node:
    """Class representing a node object used by the Board."""

    DEFAULT_RADIUS = 35
    DEFAULT_DOT_RADIUS = 16

    radius = DEFAULT_RADIUS
    dot_radius = DEFAULT_DOT_RADIUS
    highlight_color = (200, 190, 210)

    def __init__(self, x: int, y: int, canvas: tk.Canvas, id_: int):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.id = id_
        self.highlight = False
        self.color = (0, 0, 0)
        self.piece = None
        self.remove_thingy = False

        self.highlight_oval = 0
        self.remove_thingy_line1 = 0
        self.remove_thingy_line2 = 0

        self.oval = self.canvas.create_oval(self.x - Node.dot_radius - 1, self.y - Node.dot_radius - 1,
                                            self.x + Node.dot_radius, self.y + Node.dot_radius, fill="black")

    def __repr__(self):
        return f"{self.id}, {self.piece}"

    def update(self, mouse_x: int, mouse_y: int, must_remove_piece: bool, mouse_over_opponent_piece: bool):
        distance = sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        if distance <= Node.radius:
            if not self.highlight:
                self.highlight_oval = self.canvas.create_oval(self.x - Node.radius - 2, self.y - Node.radius - 2,
                                                              self.x + Node.radius, self.y + Node.radius, width=2)
                self.canvas.tag_lower(self.highlight_oval)
            self.highlight = True

            if not self.remove_thingy and must_remove_piece and mouse_over_opponent_piece:
                self.remove_thingy_line1 = self.canvas.create_line(self.x - Node.radius // 2, self.y - Node.radius // 2,
                                                                   self.x + Node.radius // 2, self.y + Node.radius // 2,
                                                                   width=2, fill="#c8bed2")
                self.remove_thingy_line2 = self.canvas.create_line(self.x + Node.radius // 2, self.y - Node.radius // 2,
                                                                   self.x - Node.radius // 2, self.y + Node.radius // 2,
                                                                   width=2, fill="#c8bed2")
            self.remove_thingy = True
        else:
            if self.highlight:
                self.canvas.delete(self.highlight_oval)
            self.highlight = False

            if self.remove_thingy and must_remove_piece and mouse_over_opponent_piece:
                self.canvas.delete(self.remove_thingy_line1)
                self.canvas.delete(self.remove_thingy_line2)
            self.remove_thingy = False

    def add_piece(self, piece):
        assert piece is not None

        self.piece = piece
        self.piece.x = self.x
        self.piece.y = self.y
        self.canvas.coords(self.piece.oval, self.piece.x - self.piece.radius - 2, self.piece.y - self.piece.radius - 2,
                           self.piece.x + self.piece.radius, self.piece.y + self.piece.radius)

    def take_piece(self, delete_oval: bool = False):
        assert self.piece is not None

        if delete_oval:
            self.canvas.delete(self.piece.oval)
            self.canvas.delete(self.remove_thingy_line1)
            self.canvas.delete(self.remove_thingy_line2)
        self.piece = None

    def change_color(self, color: str):
        """Change color of the node. It is limited to red, green and black.

        Args:
            color: The color in hex of the node.

        """
        if color == "#00ff00":
            col = (0, 255, 0)
        elif color == "#ff0000":
            col = (255, 0, 0)
        else:
            col = (0, 0, 0)
        self.color = col
        self.canvas.itemconfig(self.oval, fill=color)

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
