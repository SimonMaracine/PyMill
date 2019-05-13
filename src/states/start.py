import pygame
from src import display
from src import state_manager
from src.constants import *


def init(*args):
    global start, window, table
    start = state_manager.State(2, display.clock)
    window = display.window


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
