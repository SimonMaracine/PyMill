import time
import configparser
from os.path import join

import pygame
from src import display
from src import state_manager
from src.game_objects.board import Board
from src.gui.button import TextButton
from src.constants import *
from src.states import pause
from ..helpers import serialize, deserialize, str_to_tuple
from src.fonts import small_button_font


class MorrisNet:

    def __init__(self, *args):
        self.mode = args[0]
        self.host = args[1]
        self.client = args[2]
        self.turn = CLIENT
        self.change_turn = False

        if self.mode == HOST:
            self.board = Board()
            self.host.send(serialize((self.board, self.change_turn)))
            time.sleep(0.3)
        else:
            self.board = Board()
            self.client.send(serialize((self.board, self.change_turn)))

        button1 = TextButton(4, 16, "PAUSE", small_button_font, (255, 0, 0))
        self.buttons = (button1,)

        config = configparser.ConfigParser()
        config.read(join("data", "settings.ini"))
        bg_color = config.get("theme", "bgcolor")
        self.bg_color = str_to_tuple(bg_color)

    def render(self, surface):
        surface.fill(self.bg_color)
        self.board.render(surface)
        for btn in self.buttons:
            btn.render(surface)

    def update(self, control):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.mode == self.turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    morris_net.switch_state(EXIT, control)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not mouse_pressed[0]:
                        if self.board.clicked_on_node():
                            self.board.node_pressed = True
                        if not self.board.must_remove_piece:
                            if self.board.phase == PHASE2:
                                self.board.pick_up_piece()
                    if any(map(lambda button: button.hovered(mouse), self.buttons)):
                        TextButton.button_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if mouse_pressed[0]:
                        if self.board.must_remove_piece:
                            if self.board.node_pressed:
                                self.board.remove_opponent_piece()
                                self.change_turn = True
                        if self.board.phase == PHASE1:
                            if self.board.node_pressed:
                                self.board.put_new_piece()
                                if not self.board.must_remove_piece:
                                    self.change_turn = True
                        else:
                            if self.board.put_down_piece():  # returns if we must change the self.turn
                                if not self.board.must_remove_piece:
                                    self.change_turn = True
                    self.board.node_pressed = False

                    if self.buttons[0].pressed(mouse, mouse_pressed):
                        pause.run(control, display.window.copy())
                    TextButton.button_down = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pause.run(control, display.window.copy())

            self.board.update(mouse, mouse_pressed)
            for btn in self.buttons:
                btn.update(mouse)

            if self.board.game_over:
                morris_net.switch_state(MORRIS_HOTSEAT_STATE, control)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    morris_net.switch_state(EXIT, control)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if any(map(lambda button: button.hovered(mouse), self.buttons)):
                        TextButton.button_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.buttons[0].pressed(mouse, mouse_pressed):
                        pause.run(control, display.window.copy())
                    TextButton.button_down = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pause.run(control, display.window.copy())

            for btn in self.buttons:
                btn.update(mouse)

        if self.mode == HOST:
            if self.turn != self.mode:
                self.board, self.change_turn = deserialize(self.host.receive())
            else:
                self.host.send(serialize((self.board, self.change_turn)))
                if self.change_turn:
                    time.sleep(0.1)
        else:
            if self.turn != self.mode:
                self.board, self.change_turn = deserialize(self.client.receive())
            else:
                self.client.send(serialize((self.board, self.change_turn)))
                if self.change_turn:
                    time.sleep(0.1)

        if self.change_turn:
            self.turn = self.switch_turn()
            self.change_turn = False

        print("HOST" if self.turn == HOST else "CLIENT")

    def switch_turn(self) -> int:
        if self.turn == HOST:
            return CLIENT
        else:
            return HOST


def run(control):
    global morris_net
    morris_net = state_manager.State(MORRIS_NET_STATE, MorrisNet(), display.clock)
    morris_net.show_fps = True
    morris_net.set_frame_rate(48)
    morris_net.run(control, display.window)
