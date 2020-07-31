import tkinter as tk
from typing import Callable

from src.game.game import Game
from src.constants import *


class PyMillHotseat(Game):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable):
        super().__init__(top_level, on_game_exit)
        self.top_level.title("PyMill Hotseat")

    def on_mouse_pressed(self, event):
        if self.board.mouse_over_any_node():
            self.board.node_pressed = True
        if not self.board.game_over:  # This is for when it's a tie
            if not self.board.must_remove_piece:
                if self.board.phase == PHASE2:
                    self.board.pick_up_piece()

    def on_mouse_released(self, event):
        if not self.board.game_over:  # This is for when it's a tie
            if self.board.must_remove_piece:
                if self.board.node_pressed:
                    self.board.remove_opponent_piece()
            if self.board.phase == PHASE1:
                if self.board.node_pressed:
                    self.board.put_new_piece()
            else:
                self.board.put_down_piece()

        self.board.node_pressed = False

        self.check_for_game_over()
        self.update_gui()

    def on_mouse_moved(self, event):
        self.board.update(event.x, event.y)
