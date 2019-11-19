import configparser
from os.path import join

import pygame

from src import display
from src.game_objects.board import Board
from src.gui.button import TextButton
from src.constants import *
from src.states import pause
from src.helpers import str_to_tuple
from src.states import game_over
from src.fonts import small_button_font
from src.state_manager import State


class MorrisHotseat(State):

    def __init__(self, id_, control):
        super().__init__(id_, control)

        self.board = Board()
        self.button1 = TextButton(4, 16, "PAUSE", small_button_font, (255, 0, 0))
        self.buttons = (self.button1,)

        self.bg_color = str_to_tuple(MorrisHotseat.get_background_color())  # todo make fallback color

    def on_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.switch_state(EXIT, self._control)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if self.board.clicked_on_node():
                        self.board.node_pressed = True
                    if not self.board.must_remove_piece:
                        if self.board.phase == PHASE2:
                            self.board.pick_up_piece()
                if any(map(lambda button: button.hovered(event.pos), self.buttons)):
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT:
                    if self.board.must_remove_piece:
                        if self.board.node_pressed:
                            self.board.remove_opponent_piece()
                    if self.board.phase == PHASE1:
                        if self.board.node_pressed:
                            self.board.put_new_piece()
                    else:
                        self.board.put_down_piece()
                self.board.node_pressed = False

                if self.buttons[0].pressed(event.pos, event.button):
                    pause.run(self._control, display.window.copy())
                TextButton.button_down = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pause.run(self._control, display.window.copy())

    def update(self):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        self.board.update(mouse, mouse_pressed)
        for btn in self.buttons:
            btn.update(mouse)

        if self.board.game_over:
            game_over.run(self._control, display.window.copy(), self.board.winner)

    def render(self, surface):
        surface.fill(self.bg_color)
        self.board.render(surface)
        for btn in self.buttons:
            btn.render(surface)

    @staticmethod
    def get_background_color() -> str:
        config = configparser.ConfigParser()
        config.read(join("data", "settings.ini"))
        return config.get("theme", "bgcolor")


def run(control):
    morris = MorrisHotseat(MORRIS_HOTSEAT_STATE, control)
    morris.run()
