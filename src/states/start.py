import pygame
from src import display
from src import state_manager
from src.button import Button
from src.constants import *


def init(*args):
    global start, window, buttons
    start = state_manager.State(2, display.clock)
    window = display.window

    button1 = Button()
    button2 = Button()
    button3 = Button()
    buttons = (button1, button2, button3)


def render():
    pass


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start.exit()
            control["running"] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass


def run(control, *args):
    init()

    while start.run:
        window.fill((0, 0, 0))
        update(control)
        render()
        pygame.display.flip()
        start.tick()
