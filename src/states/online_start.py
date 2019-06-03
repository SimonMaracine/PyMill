import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.button import Button, TextButton
from src.constants import *


def init():
    global buttons
    button_font = pygame.font.SysFont("calibri", 50, True)
    buttons = ()


def render(surface):
    for btn in buttons:
        btn.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            online_start.switch_state(EXIT, control)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # if buttons[0].pressed(mouse, mouse_pressed):
            #     pass
            # elif buttons[1].pressed(mouse, mouse_pressed):
            #     pass
            # elif buttons[2].pressed(mouse, mouse_pressed):
            #     pass
            Button.button_down = False
            TextButton.button_down = False

    for btn in buttons:
        btn.update(mouse)


def run(control):
    global online_start
    online_start = state_manager.State(600, init, update, render, display.clock)
    online_start.run(control, display.window)
