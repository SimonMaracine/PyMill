import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.gui.button import Button, TextButton
from src.constants import *
from src.fonts import button_font
from src.state_manager import State


class PauseNet(State):

    def __init__(self, *args):
        self.last_frame = args[0]
        self.client = args[1]
        self.host = args[2]
        button1 = TextButton(WIDTH // 2, HEIGHT // 2 - 50, "OPTIONS", button_font, (255, 0, 0)).offset(0)
        button2 = TextButton(WIDTH // 2, HEIGHT // 2, "EXIT TO MENU", button_font, (255, 0, 0)).offset(0)
        button3 = TextButton(WIDTH // 2, HEIGHT // 2 + 50, "BACK", button_font, (255, 0, 0)).offset(0)
        self.buttons = (button1, button2, button3)
        self.background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        self.background.fill(BACKGROUND_COLOR)

    def render(self, surface):
        surface.blit(self.last_frame, (0, 0))
        surface.blit(self.background, (WIDTH // 4, HEIGHT // 4))
        for btn in self.buttons:
            btn.render(surface)

    def update(self, control):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause_net.switch_state(EXIT, control)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if any(map(lambda button: button.hovered(mouse), self.buttons)):
                    Button.button_down = True
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].pressed(mouse, mouse_pressed):
                    pass
                elif self.buttons[1].pressed(mouse, mouse_pressed):
                    pause_net.switch_state(MENU_STATE, control)
                    self.host.disconnect = True
                    self.client.disconnect = True
                elif self.buttons[2].pressed(mouse, mouse_pressed):
                    pause_net.exit()
                Button.button_down = False
                TextButton.button_down = False

        for btn in self.buttons:
            btn.update(mouse)


def run(control, *args):
    global pause_net
    pause_net = state_manager.NewState(PAUSE_STATE, PauseNet(*args), display.clock)
    pause_net.run(control, display.window)
