import threading
import tkinter as tk
from typing import Callable

from src.networking.server import Server
from src.networking.client import Client
from src.game.game import Game
from src.constants import *


class PyMillNetwork(Game):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable, client: Client, server: Server = None):
        super().__init__(top_level, on_game_exit)
        self.client = client
        self.server = server  # Keep a reference to the server to close it after finishing game TODO clean up server
        self.top_level.title("PyMill Network")

        self.lock = threading.Lock()
        self.message = None

        threading.Thread(target=self.listen_for_events, daemon=True).start()
        self.update_board_from_server()

        self.update_piece_animation()

        # self.player = TODO restrict player from doing something while it's other's turn

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
                    node_id = self.board.remove_opponent_piece()
                    if node_id != -1:
                        self.client.send_event(REMOVE_PIECE, node_id)
            if self.board.phase == PHASE1:
                if self.board.node_pressed:
                    node_id = self.board.put_new_piece()
                    if node_id != -1:
                        self.client.send_event(PLACE_PIECE, node_id)
            else:
                src_node_id, dest_node_id = self.board.put_down_piece()
                if src_node_id != -1 and dest_node_id != -1:
                    self.client.send_event(MOVE_PIECE, src_node_id, dest_node_id)

        self.board.node_pressed = False

        self.check_for_game_over()
        self.update_gui()

    def on_mouse_moved(self, event):
        self.board.update(event.x, event.y)

    def listen_for_events(self):
        # Listen for events in a separate thread, but do the action in main thread in update_board_from_server
        while True:  # TODO check when the PyMillNetwork is closed
            message = self.client.receive_event()
            with self.lock:
                self.message = message

    def update_board_from_server(self):
        with self.lock:
            if self.message is not None:
                if self.message.action == PLACE_PIECE:
                    self.board.put_new_piece_alone(self.message.args[0], WHITE if self.board.turn == PLAYER1 else BLACK)
                    print("PLACE PIECE")
                    self.message = None
                elif self.message.action == MOVE_PIECE:
                    self.board.change_piece_location(*self.message.args)
                    print("MOVE PIECE")
                    self.message = None
                elif self.message.action == REMOVE_PIECE:
                    self.board.remove_opponent_piece_alone(self.message.args[0])
                    print("REMOVE PIECE")
                    self.message = None
                elif self.message.action == CLOSE_CONNECTION:
                    print("CLOSE CONNECTION REQUESTED")
                    self.message = None

                self.check_for_game_over()
                self.update_gui()

        self.after(100, self.update_board_from_server)

    def update_piece_animation(self):
        for node in self.board.nodes:
            if node.piece is not None and not node.piece.reached_position:
                node.piece.update(0, 0)
        self.after(25, self.update_piece_animation)
