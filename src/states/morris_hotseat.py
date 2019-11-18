import configparser
from os.path import join

import pygame
from src import display
from src import state_manager
from src.game_objects.board import Board
from src.gui.button import TextButton
from src.constants import *
from src.states import pause
from src.helpers import str_to_tuple
from src.states import game_over
from src.fonts import small_button_font
from src.state_manager import State


class MorrisHotseat(State):

    def __init__(self):
        self.board = Board()
        self.button1 = TextButton(4, 16, "PAUSE", small_button_font, (255, 0, 0))
        self.buttons = (self.button1,)

        self.config = configparser.ConfigParser()
        self.config.read(join("data", "settings.ini"))
        bg_color = self.config.get("theme", "bgcolor")
        self.bg_color = str_to_tuple(bg_color)  # todo make fallback color

    def render(self, surface):
        surface.fill(self.bg_color)
        self.board.render(surface)
        for btn in self.buttons:
            btn.render(surface)

    def update(self, control):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                morris.switch_state(EXIT, control)
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
                    if self.board.phase == PHASE1:
                        if self.board.node_pressed:
                            self.board.put_new_piece()
                    else:
                        self.board.put_down_piece()
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
            game_over.run(control, display.window.copy(), self.board.winner)


def run(control):
    global morris
    morris = state_manager.NewState(MORRIS_HOTSEAT_STATE, MorrisHotseat(), display.clock)
    morris.show_fps = True
    morris.run(control, display.window)
