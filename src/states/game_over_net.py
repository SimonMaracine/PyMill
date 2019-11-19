import logging
import pygame

from src.display import WIDTH, HEIGHT
from src.gui.button import Button, TextButton
from src.constants import *
from src.fonts import button_font, title_font
from src.log import get_logger
from src.state_manager import State

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


class GameOverNet(State):

    def __init__(self, id_, control, *args):
        super().__init__(id_, control)

        self.last_frame = args[0]
        self.winner = args[1]
        self.client = args[2]
        self.host = args[3]
        button1 = TextButton(WIDTH // 2, HEIGHT // 2, "PLAY AGAIN", button_font, (255, 0, 0)).offset(0)
        button2 = TextButton(WIDTH // 2, HEIGHT // 2 + 50, "EXIT TO MENU", button_font, (255, 0, 0)).offset(0)
        self.buttons = (button1, button2)
        self.background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        self.background.fill(BACKGROUND_COLOR)
        self.who_won = title_font.render(f"{'White' if self.winner == WHITE else 'Black'} won!", True, (0, 0, 0))
        logger.debug(f"Winner is {self.winner}")

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
                    pass
                elif self.buttons[1].pressed(event.pos, event.button):
                    self.switch_state(MENU_STATE, self._control)
                    self.host.disconnect = True
                    self.client.disconnect = True
                    logger.debug("Stopping the server and client")
                Button.button_down = False
                TextButton.button_down = False

    def update(self):
        mouse = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update(mouse)

    def render(self, surface):
        surface.blit(self.last_frame, (0, 0))
        surface.blit(self.background, (WIDTH // 4, HEIGHT // 4))
        surface.blit(self.who_won, (WIDTH // 2 - self.who_won.get_width() // 2, HEIGHT // 2 - 90))
        for btn in self.buttons:
            btn.render(surface)


def run(control, *args):
    game_over_net = GameOverNet(GAME_OVER_STATE, control, *args)
    game_over_net.run()
