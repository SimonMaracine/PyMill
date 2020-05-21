import tkinter as tk
from typing import Callable

from src.game.game import Game
from src.constants import *
from src.game.minimax import ai_place_piece_at, ai_remove_piece, ai_move_piece


class PyMillComputer(Game):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable):
        super().__init__(top_level, on_game_exit)
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
        self.canvas.update_idletasks()
        self.make_computer_move()

        self.check_for_game_over()
        self.update_gui()

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
        self.after(10, self.update_piece_animation)


# def pymill_computer(on_game_exit: Callable):
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
#
#     running = True
#
#     while running:
#         if board.turn == PLAYER2 and not board.game_over:
#             if board.phase == PHASE1:
#                 print("Making a move...")
#                 board.put_new_piece_alone(ai_place_piece_at(board.get_current_state()), BLACK)
#                 if board.must_remove_piece:
#                     board.remove_opponent_piece_alone(ai_remove_piece())
#             else:
#                 # if not board.game_over:
#                 print("Making a move...")
#                 board.change_piece_location(*ai_move_piece(board.get_current_state()))
#                 if board.must_remove_piece:
#                     board.remove_opponent_piece_alone(ai_remove_piece())
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#             if board.turn == PLAYER1 and not board.game_over:
#                 if event.type == pygame.MOUSEBUTTONDOWN:
#                     if event.button == pygame.BUTTON_LEFT:
#                         if board.mouse_over_any_node():
#                             board.node_pressed = True
#                         if not board.must_remove_piece:
#                             if board.phase == PHASE2:
#                                 board.pick_up_piece()
#                 elif event.type == pygame.MOUSEBUTTONUP:
#                     if event.button == pygame.BUTTON_LEFT:
#                         if board.must_remove_piece:
#                             if board.node_pressed:
#                                 board.remove_opponent_piece()
#                         if board.phase == PHASE1:
#                             if board.node_pressed:
#                                 board.put_new_piece()
#                         else:
#                             board.put_down_piece()
#                     board.node_pressed = False
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_MINUS:
#                         if current_scale > 1:
#                             width -= 160
#                             height -= 120
#                             window = pygame.display.set_mode((width, height))  # TODO also resize the text
#                             board.on_window_resize(width, height)
#                             current_scale -= 1
#                     elif event.key == pygame.K_EQUALS:
#                         if current_scale < 5:
#                             width += 160
#                             height += 120
#                             window = pygame.display.set_mode((width, height))
#                             board.on_window_resize(width, height)
#                             current_scale += 1
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
