import tkinter as tk
from typing import Callable

from src.game.board import Board
from src.constants import *


class PymillHotseat(tk.Frame):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable):
        super().__init__(top_level)
        self.top_level = top_level
        self.on_game_exit = on_game_exit
        self.pack(padx=10, pady=10, expand=True)

        self.top_level.title("Pymill Hotseat")
        self.top_level.wm_protocol("WM_DELETE_WINDOW", self.exit)

        self.canvas = tk.Canvas(self, width=800, height=800, background="#ffe48a")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_mouse_pressed)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_released)
        self.canvas.bind("<Motion>", self.on_mouse_moved)

        self.board = Board(self.canvas)

    def on_mouse_pressed(self, event):
        if self.board.mouse_over_any_node():
            self.board.node_pressed = True
        if not self.board.must_remove_piece:
            if self.board.phase == PHASE2:
                self.board.pick_up_piece()

    def on_mouse_released(self, event):
        if self.board.must_remove_piece:
            if self.board.node_pressed:
                self.board.remove_opponent_piece()
        if self.board.phase == PHASE1:
            if self.board.node_pressed:
                self.board.put_new_piece()
        else:
            self.board.put_down_piece()

        self.board.node_pressed = False

    def on_mouse_moved(self, event):
        self.board.update(event.x, event.y)

    def exit(self):
        self.top_level.destroy()
        self.on_game_exit()


# def pymill_hotseat(on_game_exit: Callable):
#     width = 800
#     height = 600
#     current_scale = 1
#
#     pygame.display.init()
#     pygame.font.init()
#
#     window = pygame.display.set_mode((width, height))
#     pygame.display.set_caption("PyMill")
#     clock = pygame.time.Clock()
#
#     board = Board()
#     running = True
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == pygame.BUTTON_LEFT:
#                     if board.mouse_over_any_node():
#                         board.node_pressed = True
#                     if not board.must_remove_piece:
#                         if board.phase == PHASE2:
#                             board.pick_up_piece()
#             elif event.type == pygame.MOUSEBUTTONUP:
#                 if event.button == pygame.BUTTON_LEFT:
#                     if board.must_remove_piece:
#                         if board.node_pressed:
#                             board.remove_opponent_piece()
#                     if board.phase == PHASE1:
#                         if board.node_pressed:
#                             board.put_new_piece()
#                     else:
#                         board.put_down_piece()
#                 board.node_pressed = False
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_MINUS:
#                     if current_scale > 1:
#                         width -= 160
#                         height -= 120
#                         window = pygame.display.set_mode((width, height))  # TODO also resize the text
#                         board.on_window_resize(width, height)
#                         current_scale -= 1
#                 elif event.key == pygame.K_EQUALS:
#                     if current_scale < 5:
#                         width += 160
#                         height += 120
#                         window = pygame.display.set_mode((width, height))
#                         board.on_window_resize(width, height)
#                         current_scale += 1
#
#         mouse = pygame.mouse.get_pos()
#         board.update(mouse)
#
#         if board.game_over:
#             print("GAME OVER")
#
#         window.fill((148, 16, 148))
#         board.render(window)
#         pygame.display.flip()
#         clock.tick(30)
#
#     on_game_exit()
#     pygame.quit()
