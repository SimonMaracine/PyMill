import logging
import pygame

from src.display import WIDTH, HEIGHT
from src.gui.button import Button, TextButton
from src.constants import *
from src.fonts import button_font, small_title_font
from src.log import get_logger
from src.state_manager import State

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


class TheOtherDisconnected(State):

    def __init__(self, id_, control):
        super().__init__(id_, control)

        self.last_frame = control.args[0]

        button1 = TextButton(WIDTH // 2, HEIGHT // 2 + 50, "EXIT TO MENU", button_font, (255, 0, 0)).offset(0)
        self.buttons = (button1,)
        self.background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        self.background.fill(BACKGROUND_COLOR)
        self.who_won = small_title_font.render("Connection lost", True, (0, 0, 0))

    def on_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.switch_state(EXIT, self._control)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if any(map(lambda button: button.hovered(event.pos), self.buttons)):
                    Button.button_down = True
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].pressed(event.pos, event.button):
                    self.switch_state(MENU_STATE, self._control)
                Button.button_down = False
                TextButton.button_down = False

    def update(self):
        mouse = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update(mouse)

    def render(self, surface):
        surface.blit(self.last_frame, (0, 0))
        surface.blit(self.background, (WIDTH // 4, HEIGHT // 4))
        surface.blit(self.who_won, (WIDTH // 2 - self.who_won.get_width() // 2, HEIGHT // 2 - 50))
        for btn in self.buttons:
            btn.render(surface)

    def on_exit(self):
        pass


def run(control):
    the_other_disconnected = TheOtherDisconnected(THE_OTHER_DISCONNECTED, control)
    the_other_disconnected.run()
