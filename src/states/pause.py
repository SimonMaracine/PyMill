import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.button import Button, TextButton
from src.constants import *


def init():
    global buttons
    button_font = pygame.font.SysFont("calibri", 50, True)
    button1 = TextButton(WIDTH // 2, HEIGHT // 2 - 75, "OPTIONS", button_font, (255, 0, 0)).offset(0)
    button2 = TextButton(WIDTH // 2, HEIGHT // 2 - 25, "EXIT TO MENU", button_font, (255, 0, 0)).offset(0)
    button3 = TextButton(WIDTH // 2, HEIGHT // 2 + 25, "BACK", button_font, (255, 0, 0)).offset(0)
    buttons = (button1, button2, button3)


def render(surface):
    for btn in buttons:
        btn.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pause.exit()
            control["running"] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttons[0].pressed(mouse, mouse_pressed):
                pass
            elif buttons[1].pressed(mouse, mouse_pressed):
                pause.switch_state(MENU_STATE, control)
            elif buttons[2].pressed(mouse, mouse_pressed):
                pause.exit()
            Button.button_down = False
            TextButton.button_down = False

    for btn in buttons:
        btn.update(mouse)


def run(control):
    global pause
    pause = state_manager.State(6, init, update, render, display.clock)
    pause.run(control, display.window)