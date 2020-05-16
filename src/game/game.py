import tkinter as tk
from tkinter import messagebox
from typing import Callable
from abc import abstractmethod, ABC

from src.game.board import Board
from src.constants import *


class Game(ABC, tk.Frame):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable):
        super().__init__(top_level)
        self.top_level = top_level
        self.on_game_exit = on_game_exit
        self.pack(padx=10, pady=10, expand=True)

        self.top_level.title("PyMill Hotseat")
        self.top_level.wm_protocol("WM_DELETE_WINDOW", self.exit)

        self.canvas = tk.Canvas(self, width=800, height=800, background="#ffe48a")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_mouse_pressed)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_released)
        self.canvas.bind("<Motion>", self.on_mouse_moved)

        self.board = Board(self.canvas)
        self.game_over = False

    @abstractmethod
    def on_mouse_pressed(self, event):
        pass

    @abstractmethod
    def on_mouse_released(self, event):
        pass

    @abstractmethod
    def on_mouse_moved(self, event):
        pass

    def check_for_game_over(self):
        if not self.game_over and self.board.game_over:
            if self.board.winner != TIE:
                messyge = f"{'White' if self.board.winner == PLAYER1 else 'Black'} has won!"
            else:
                messyge = "Tie between both players!"

            messagebox.showinfo(title="Game Over", message=messyge, parent=self.top_level)
            self.game_over = True

    def exit(self):
        self.top_level.destroy()
        self.on_game_exit()
