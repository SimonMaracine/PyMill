import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.gui.button import Button, TextButton
from src.constants import *


def init():
    global buttons
    button_font = pygame.font.SysFont("calibri", 50, True)
    button1 = TextButton(WIDTH // 2, HEIGHT // 2 - 75, "CHANGE THEME", button_font, (255, 0, 0)).offset(0)
    button2 = TextButton(WIDTH // 2, HEIGHT // 2 - 25, "CREDITS", button_font, (255, 0, 0)).offset(0)
    button3 = TextButton(WIDTH // 2, HEIGHT // 2 + 25, "NETWORKING", button_font, (255, 0, 0)).offset(0)
    button4 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
    buttons = (button1, button2, button3, button4)


def render(surface):
    surface.fill(BACKGROUND_COLOR)
    for btn in buttons:
        btn.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            options.switch_state(EXIT, control)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttons[0].pressed(mouse, mouse_pressed):
                pass
            elif buttons[1].pressed(mouse, mouse_pressed):
                pass
            elif buttons[2].pressed(mouse, mouse_pressed):
                options.switch_state(NETSETTINGS_STATE, control)
            elif buttons[3].pressed(mouse, mouse_pressed):
                options.switch_state(MENU_STATE, control)
            Button.button_down = False
            TextButton.button_down = False

    for btn in buttons:
        btn.update(mouse)


def run(control):
    global options
    options = state_manager.State(OPTIONS_STATE, init, update, render, display.clock)
    options.run(control, display.window)
