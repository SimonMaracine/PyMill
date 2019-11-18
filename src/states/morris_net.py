import time
import configparser
import logging
import tkinter as tk
from os.path import join

import pygame

from src import display
from src import state_manager
from src.game_objects.board import Board
from src.gui.button import TextButton
from src.constants import *
from src.states import pause_net, game_over_net, the_other_disconnected
from ..helpers import serialize, deserialize, str_to_tuple, Boolean
from src.fonts import small_button_font
from src.networking.package import Package
from src.log import get_logger
from src.tkinter_debug import tk_debug
from src.state_manager import State
logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


class MorrisNet(State):

    def __init__(self, *args):
        self.mode = args[0]
        self.host = args[1]
        self.client = args[2]
        self.turn = CLIENT
        self.change_turn = Boolean(False)
        self.board = Board()

        self.package = Package(Boolean(True), self.board, self.change_turn)

        if self.mode == HOST:
            self.host.send(serialize(self.package))
            time.sleep(0.3)
        else:
            self.client.send(serialize(self.package))

        button1 = TextButton(4, 16, "PAUSE", small_button_font, (255, 0, 0))
        self.buttons = (button1,)

        config = configparser.ConfigParser()
        config.read(join("data", "settings.ini"))
        bg_color = config.get("theme", "bgcolor")
        self.bg_color = str_to_tuple(bg_color)

        self.frame = tk_debug.DebugWindow()
        self.tk_turn = tk.StringVar(self.frame)
        tk.Label(self.frame, textvariable=self.tk_turn).pack()

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
                    self.host.disconnect = True
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
                                if self.board.remove_opponent_piece():  # returns if we could take the piece
                                    self.change_turn.set(True)
                        if self.board.phase == PHASE1:
                            if self.board.node_pressed:
                                if self.board.put_new_piece():  # returns if we must change the self.turn
                                # if not self.board.must_remove_piece:
                                    self.change_turn.set(True)
                        else:
                            if self.board.put_down_piece():  # returns if we must change the self.turn
                                if not self.board.must_remove_piece:
                                    self.change_turn.set(True)
                    self.board.node_pressed = False

                    if self.buttons[0].pressed(mouse, mouse_pressed):
                        pause_net.run(control, display.window.copy(), self.client, self.host)
                    TextButton.button_down = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pause_net.run(control, display.window.copy(), self.client, self.host)

            self.board.update(mouse, mouse_pressed)
            for btn in self.buttons:
                btn.update(mouse)

            # if self.board.game_over:
            #     logger.debug("Switching to GAME_OVER_STATE")
            #     game_over.run(control, display.window.copy(), self.board.winner)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.disconnect = True
                    morris_net.switch_state(EXIT, control)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if any(map(lambda button: button.hovered(mouse), self.buttons)):
                        TextButton.button_down = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.buttons[0].pressed(mouse, mouse_pressed):
                        pause_net.run(control, display.window.copy(), self.client, self.host)
                    TextButton.button_down = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pause_net.run(control, display.window.copy(), self.client, self.host)

            for btn in self.buttons:
                btn.update(mouse)

        if self.mode == HOST:
            if self.turn != self.mode:
                try:
                    self.package = deserialize(self.host.receive())
                except EOFError as e:
                    print(e)
                self.change_turn = self.package.change_turn
                if self.package.board is not None:
                    self.board = self.package.board
            else:
                self.host.send(serialize(self.package))
                if self.change_turn.get():
                    time.sleep(0.1)
        else:
            if self.turn != self.mode:
                try:
                    self.package = deserialize(self.client.receive())
                except EOFError as e:
                    print(e)
                self.change_turn = self.package.change_turn
                if self.package.board is not None:
                    self.board = self.package.board
            else:
                self.client.send(serialize(self.package))
                if self.change_turn.get():
                    time.sleep(0.1)

        if self.change_turn.get():
            self.turn = self.switch_turn()
            self.change_turn.set(False)

        if self.board.game_over:
            logger.debug("Switching to GAME_OVER_STATE")
            game_over_net.run(control, display.window.copy(), self.board.winner, self.client, self.host)

        if self.mode == HOST:
            if self.client.disconnect:
                print("CLIENT GONE")
                the_other_disconnected.run(control, display.window.copy())
        else:
            if self.host.disconnect:
                print("HOST GONE")
                the_other_disconnected.run(control, display.window.copy())

        self.tk_turn.set(("HOST" if self.turn == HOST else "CLIENT") + " is making a move")
        tk_debug.update()

    def switch_turn(self) -> int:
        if self.turn == HOST:
            return CLIENT
        else:
            return HOST


def run(control):
    global morris_net
    morris_net = state_manager.NewState(MORRIS_NET_STATE, MorrisNet(*control["args"]), display.clock)
    morris_net.show_fps = True
    morris_net.run(control, display.window)
