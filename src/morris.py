import pygame
import display
from state_manager import State


def init():
    global morris, window
    morris = State(1, display.clock)
    window = display.window
    morris.set_frame_rate(60)


def render():
    pygame.draw.rect(window, (0, 0, 0), (20, 20, 140, 80))


def update(control):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            morris.exit()
            control["running"] = False


def run(control):
    init()

    while morris.run:
        window.fill((130, 0, 130))
        update(control)
        render()
        pygame.display.flip()
        morris.clock.tick(morris.fps)
