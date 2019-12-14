import pygame

from src.display import WIDTH, HEIGHT
from src.gui.button import Button, TextButton
from src.constants import *
from src.fonts import button_font
from src.state_manager import State


class PauseNet(State):

    def __init__(self, id_, control):
        super().__init__(id_, control)

        self.last_frame = control.args[0]
        self.thing = control.args[1]  # client or server

        button1 = TextButton(WIDTH // 2, HEIGHT // 2 - 50, "OPTIONS", button_font, (255, 0, 0)).offset(0)
        button2 = TextButton(WIDTH // 2, HEIGHT // 2, "EXIT TO MENU", button_font, (255, 0, 0)).offset(0)
        button3 = TextButton(WIDTH // 2, HEIGHT // 2 + 50, "BACK", button_font, (255, 0, 0)).offset(0)
        self.buttons = (button1, button2, button3)
        self.background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        self.background.fill(BACKGROUND_COLOR)

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
                    self.thing.disconnect = True
                    self.on_exit()
                elif self.buttons[2].pressed(event.pos, event.button):
                    self.exit()
                Button.button_down = False
                TextButton.button_down = False

    def update(self):
        mouse = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update(mouse)

    def render(self, surface):
        surface.blit(self.last_frame, (0, 0))
        surface.blit(self.background, (WIDTH // 4, HEIGHT // 4))
        for btn in self.buttons:
            btn.render(surface)

    def on_exit(self):
        pass


def run(control, *args):
    control.args = args
    pause_net = PauseNet(PAUSE_STATE, control)
    pause_net.run()
