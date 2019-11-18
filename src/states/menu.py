import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.gui.button import TextButton
from src.constants import *
from src.fonts import button_font
from src.state_manager import State


class Menu(State):

    def __init__(self):
        button1 = TextButton(WIDTH // 2, HEIGHT // 2 - 75, "PLAY", button_font, (255, 0, 0)).offset(0)
        button2 = TextButton(WIDTH // 2, HEIGHT // 2 - 25, "OPTIONS", button_font, (255, 0, 0)).offset(0)
        button3 = TextButton(WIDTH // 2, HEIGHT // 2 + 25, "QUIT", button_font, (255, 0, 0)).offset(0)
        self.buttons = (button1, button2, button3)
        # for btn in buttons:
        #     btn.render_background = True  # todo work on this

    def render(self, surface):
        surface.fill(BACKGROUND_COLOR)
        for btn in self.buttons:
            btn.render(surface)

    def update(self, control):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu.switch_state(EXIT, control)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if any(map(lambda button: button.hovered(mouse), self.buttons)):
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].pressed(mouse, mouse_pressed):
                    menu.switch_state(START_STATE, control)
                elif self.buttons[1].pressed(mouse, mouse_pressed):
                    menu.switch_state(OPTIONS_STATE, control)
                elif self.buttons[2].pressed(mouse, mouse_pressed):
                    menu.switch_state(EXIT, control)
                TextButton.button_down = False

        for btn in self.buttons:
            btn.update(mouse)


def run(control):
    global menu
    menu = state_manager.NewState(MENU_STATE, Menu(), display.clock)
    menu.run(control, display.window)

