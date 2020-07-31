import tkinter as tk
from typing import Callable

from src.game.game import Game
from src.constants import *
# from src.minimax.minimax import ai_place_piece_at, ai_remove_piece, ai_move_piece
from minimax import ai_place_piece_at, ai_remove_piece, ai_move_piece


class PyMillComputer(Game):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable):
        super().__init__(top_level, on_game_exit)
        self.top_level.title("PyMill Computer")
        self.update_piece_animation()

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

        self.update_gui()
        self.top_level.config(cursor="watch")  # Change the cursor to busy
        self.canvas.update_idletasks()
        self.make_computer_move()

        self.check_for_game_over()
        self.update_gui()
        self.top_level.config(cursor="")

    def on_mouse_moved(self, event):
        self.board.update(event.x, event.y)

    def make_computer_move(self):
        if self.board.turn == PLAYER2 and not self.board.game_over:
            if self.board.phase == PHASE1:
                print("Making a move...")
                self.board.put_new_piece_alone(ai_place_piece_at(self.board.get_current_state()), BLACK)
                if self.board.must_remove_piece:
                    self.board.remove_opponent_piece_alone(ai_remove_piece())
            else:
                print("Making a move...")
                self.board.change_piece_location(*ai_move_piece(self.board.get_current_state()))
                if self.board.must_remove_piece:
                    self.board.remove_opponent_piece_alone(ai_remove_piece())

    def update_piece_animation(self):
        for node in self.board.nodes:
            if node.piece is not None and not node.piece.reached_position:
                node.piece.update(0, 0)
        self.after(25, self.update_piece_animation)
