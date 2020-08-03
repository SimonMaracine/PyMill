import tkinter as tk
from tkinter import messagebox
from typing import Callable
from abc import abstractmethod, ABC

from src.game.board import Board
from src.constants import *


class Game(ABC, tk.Frame):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable):
        super().__init__(top_level)  # This calls Frame's __init__
        self.top_level = top_level
        self.on_game_exit = on_game_exit
        self.pack(padx=10, pady=10, expand=True)

        self.canvas_width = 700

        self.top_level.wm_protocol("WM_DELETE_WINDOW", self.exit)

        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_width, background="#ffe48a")  # , highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.canvas.addtag_all("all")

        self.canvas.bind("<Button-1>", self.on_mouse_pressed)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_released)
        self.canvas.bind("<Motion>", self.on_mouse_moved)

        self.bind("<Configure>", self.on_resize)

        self.dont_resize = True

        self.var_player1_pieces_left = tk.StringVar(self, "White pieces: 9")
        self.lbl_player1_pieces_left = tk.Label(self, textvariable=self.var_player1_pieces_left, font="TkDefaultFont 10 bold")
        self.var_player2_pieces_left = tk.StringVar(self, "Black pieces: 9")
        self.lbl_player2_pieces_left = tk.Label(self, textvariable=self.var_player2_pieces_left, font="TkDefaultFont 10 bold")

        self.lbl_player1_pieces_left.grid(row=1, column=0)
        self.lbl_player2_pieces_left.grid(row=1, column=2)

        self.var_current_player = tk.StringVar(self, "White's turn")
        tk.Label(self, textvariable=self.var_current_player, font="TkDefaultFont 10 bold").grid(row=1, column=1)

        self.board = Board(self.canvas, self.canvas_width)
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

    def on_resize(self, event):
        smallest = min(event.width, event.height - 22)

        try:
            scale = smallest / self.canvas_width
        except ZeroDivisionError:
            return

        self.canvas_width = smallest
        self.board.canvas_width = smallest
        if not self.dont_resize:
            self.canvas.config(width=smallest, height=smallest)
        self.config(width=smallest, height=smallest)
        self.dont_resize = False

        if scale == 0:
            return

        # Rescale all the objects tagged with the "all" tag
        self.canvas.scale("all", 0, 0, scale, scale)

        self.board.on_window_resize(smallest)

    def check_for_game_over(self):
        if not self.game_over and self.board.game_over:
            if self.board.winner != TIE:
                messyge = f"{'White' if self.board.winner == PLAYER1 else 'Black'} has won!"
            else:
                messyge = "Tie between both players!"

            messagebox.showinfo(title="Game Over", message=messyge, parent=self.top_level)
            self.game_over = True

    def update_gui(self):
        self.var_player1_pieces_left.set(f"White pieces: {self.board.white_pieces}")
        self.var_player2_pieces_left.set(f"Black pieces: {self.board.black_pieces}")
        self.var_current_player.set("White's turn" if self.board.turn == PLAYER1 else "Black's turn")

        player1_pieces = int(self.var_player1_pieces_left.get()[-1])
        player2_pieces = int(self.var_player2_pieces_left.get()[-1])

        if player1_pieces == player2_pieces == 0:
            self.lbl_player1_pieces_left.grid_remove()
            self.lbl_player2_pieces_left.grid_remove()

    def exit(self):
        self.top_level.destroy()
        self.on_game_exit()
