import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.gui.button import Button, TextButton
from src.constants import *
from src.fonts import button_font

last_frame: pygame.Surface


class Pause:

    def __init__(self):
        button1 = TextButton(WIDTH // 2, HEIGHT // 2 - 100, "OPTIONS", button_font, (255, 0, 0)).offset(0)
        button2 = TextButton(WIDTH // 2, HEIGHT // 2 - 50, "EXIT TO MENU", button_font, (255, 0, 0)).offset(0)
        button3 = TextButton(WIDTH // 2, HEIGHT // 2, "RESTART", button_font, (255, 0, 0)).offset(0)
        button4 = TextButton(WIDTH // 2, HEIGHT // 2 + 50, "BACK", button_font, (255, 0, 0)).offset(0)
        self.buttons = (button1, button2, button3, button4)
        self.background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
        self.background.fill(BACKGROUND_COLOR)

    def render(self, surface):
        surface.blit(last_frame, (0, 0))
        surface.blit(self.background, (WIDTH // 4, HEIGHT // 4))
        for btn in self.buttons:
            btn.render(surface)

    def update(self, control):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause.switch_state(EXIT, control)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if any(map(lambda button: button.hovered(mouse), self.buttons)):
                    Button.button_down = True
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].pressed(mouse, mouse_pressed):
                    pass
                elif self.buttons[1].pressed(mouse, mouse_pressed):
                    pause.switch_state(MENU_STATE, control)
                elif self.buttons[2].pressed(mouse, mouse_pressed):
                    pause.switch_state(MORRIS_HOTSEAT_STATE, control, True)
                elif self.buttons[3].pressed(mouse, mouse_pressed):
                    pause.exit()
                Button.button_down = False
                TextButton.button_down = False

        for btn in self.buttons:
            btn.update(mouse)


def run(control, *args):
    global pause, last_frame
    last_frame = args[0]
    pause = state_manager.State(PAUSE_STATE, Pause(), display.clock)
    pause.run(control, display.window)
