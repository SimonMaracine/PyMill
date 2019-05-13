import pygame
from src import display
from src import state_manager
from src.button import Button
from src.constants import *


def init(*args):
    global menu, window, buttons, button
    menu = state_manager.State(1, display.clock)
    window = display.window
    button_font = pygame.font.SysFont("calibri", 40)
    button = Button(40, 40, "PLAY", button_font, (255, 0, 0))
    buttons = (button,)


def render():
    for btn in buttons:
        btn.render(window)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu.exit()
            control["running"] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            if button.pressed(mouse, mouse_pressed):
                menu.switch_state(MORRIS_HOTSEAT_STATE, control)

    for btn in buttons:
        btn.update(mouse)


def run(control, *args):
    init()

    while menu.run:
        window.fill((0, 0, 0))
        update(control)
        render()
        pygame.display.flip()
        menu.tick()
