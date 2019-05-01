import pygame
from src import display
from src import state_manager
from src.table import Table
from src.piece import Piece


def init(*args):
    global morris, window, table
    morris = state_manager.State(1, display.clock)
    window = display.window
    morris.set_frame_rate(60)

    table = Table()


def render():
    table.render(window)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            morris.exit()
            control["running"] = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_pressed[0]:
                table.put_new_piece()

    table.update(mouse)


def run(control, *args):
    init()

    while morris.run:
        window.fill((160, 15, 160))
        update(control)
        render()
        pygame.display.flip()
        morris.tick()
