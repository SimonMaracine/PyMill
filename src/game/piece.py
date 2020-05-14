import tkinter as tk
from src.constants import *


class Piece:
    """Class representing a piece object used by the Board."""

    DEFAULT_RADIUS = 30

    radius = DEFAULT_RADIUS

    def __init__(self, x: int, y: int, color: tuple, canvas: tk.Canvas):
        self.x = x
        self.y = y
        self.color = color
        self.canvas = canvas
        self.picked_up = False

        self.oval = self.canvas.create_oval(self.x - Piece.radius - 2, self.y - Piece.radius - 2, self.x + Piece.radius,
                                            self.y + Piece.radius, fill="#ffe363" if self.color == WHITE else "black")

    def __repr__(self):
        return "WHITE piece" if self.color == WHITE else "BLACK piece"

    def update(self, mouse_x: int, mouse_y: int):
        if self.picked_up:
            self.x = mouse_x
            self.y = mouse_y
            self.canvas.coords(self.oval, self.x - Piece.radius - 2, self.y - Piece.radius - 2, self.x + Piece.radius,
                               self.y + Piece.radius)

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
        self.canvas.coords(self.oval, self.x - Piece.radius - 2, self.y - Piece.radius - 2, self.x + Piece.radius,
                           self.y + Piece.radius)
