import pygame

from src.display import WIDTH, HEIGHT
from src.gui.button import Button, TextButton
from src.constants import *
from src.fonts import button_font
from src.state_manager import State


class Pause(State):

    def __init__(self, id_, control, *args):
        super().__init__(id_, control)

        self.last_frame = args[0]
        button1 = TextButton(WIDTH // 2, HEIGHT // 2 - 100, "OPTIONS", button_font, (255, 0, 0)).offset(0)
        button2 = TextButton(WIDTH // 2, HEIGHT // 2 - 50, "EXIT TO MENU", button_font, (255, 0, 0)).offset(0)
        button3 = TextButton(WIDTH // 2, HEIGHT // 2, "RESTART", button_font, (255, 0, 0)).offset(0)
        button4 = TextButton(WIDTH // 2, HEIGHT // 2 + 50, "BACK", button_font, (255, 0, 0)).offset(0)
        self.buttons = (button1, button2, button3, button4)
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
                elif self.buttons[2].pressed(event.pos, event.button):
                    self.switch_state(MORRIS_HOTSEAT_STATE, self._control, True)
                elif self.buttons[3].pressed(event.pos, event.button):
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


def run(control, *args):
    pause = Pause(PAUSE_STATE, control, *args)
    pause.run()
