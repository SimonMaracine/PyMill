import pygame

from src.display import WIDTH, HEIGHT
from src.gui.button import Button, TextButton
from src.constants import *
from src.fonts import button_font
from src.state_manager import State


class Options(State):

    def __init__(self, id_, control):
        super().__init__(id_, control)

        button1 = TextButton(WIDTH // 2, HEIGHT // 2 - 75, "CHANGE THEME", button_font, (255, 0, 0)).offset(0)
        button2 = TextButton(WIDTH // 2, HEIGHT // 2 - 25, "CREDITS", button_font, (255, 0, 0)).offset(0)
        button3 = TextButton(WIDTH // 2, HEIGHT // 2 + 25, "NETWORKING", button_font, (255, 0, 0)).offset(0)
        button4 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
        self.buttons = (button1, button2, button3, button4)

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
                    pass
                elif self.buttons[2].pressed(event.pos, event.button):
                    self.switch_state(NETSETTINGS_STATE, self._control)
                elif self.buttons[3].pressed(event.pos, event.button):
                    self.switch_state(MENU_STATE, self._control)
                Button.button_down = False
                TextButton.button_down = False

    def update(self):
        mouse = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update(mouse)

    def render(self, surface):
        surface.fill(BACKGROUND_COLOR)
        for btn in self.buttons:
            btn.render(surface)


def run(control):
    options = Options(OPTIONS_STATE, control)
    options.run()
