import threading
import tkinter as tk
from tkinter import messagebox
from typing import Callable

from src.networking.server import Server
from src.networking.client import Client
from src.game.game import Game
from src.constants import *


class PyMillNetwork(Game):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable, is_first: bool, client: Client,
                 server: Server = None):
        super().__init__(top_level, on_game_exit)
        self.client = client
        self.server = server  # Keep a reference to the server to close it after finishing game
        self.top_level.title("PyMill Network")

        self.lock = threading.Lock()
        self.message = None

        self.listen_events = True

        threading.Thread(target=self.listen_for_events, daemon=True).start()
        self.update_board_from_server()

        self.update_piece_animation()

        self.player = PLAYER1 if is_first else PLAYER2  # To stop player from making a move when he/she shouldn't

    def on_mouse_pressed(self, event):
        if self.board.turn == self.player:
            if self.board.mouse_over_any_node():
                self.board.node_pressed = True
            if not self.board.game_over:  # This is for when it's a tie
                if not self.board.must_remove_piece:
                    if self.board.phase == PHASE2:
                        self.board.pick_up_piece()

    def on_mouse_released(self, event):
        if self.board.turn == self.player:
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
        if self.board.turn == self.player or self.board.mouse_over_any_node():
            self.board.update(event.x, event.y)

    def listen_for_events(self):
        # Listen for events in a separate thread, but do the action in main thread in update_board_from_server
        while self.listen_events:
            try:
                message = self.client.receive_event()
            except EOFError:  # What the socket received was nothing
                try:
                    self.client.close()  # Close the client, because the other client and the server were closed
                except OSError:  # This was the client which was closed with the server
                    pass
                self.listen_events = False
                try:
                    messagebox.showerror("Connection Lost", "The player has closed the connection.", parent=self.top_level)
                except tk.TclError:  # This was the client which was closed with the server
                    pass
                continue
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
                    self.client.close()
                    self.server.close()  # Close the client and the server, because the other client has disconnected
                    self.listen_events = False
                    print("CLOSE CONNECTION")
                    self.message = None
                    messagebox.showerror("Connection Lost", "The player has closed the connection.", parent=self.top_level)

                self.check_for_game_over()
                self.update_gui()

        self.after(100, self.update_board_from_server)

    def update_piece_animation(self):
        for node in self.board.nodes:
            if node.piece is not None and not node.piece.reached_position:
                node.piece.update(0, 0)
        self.after(25, self.update_piece_animation)

    def exit(self):
        super().exit()
        if not self.client.closed:  # The client might have been closed already in update_board_from_server
            self.client.close()
        if self.server is not None:
            self.server.close()
        self.listen_events = False
