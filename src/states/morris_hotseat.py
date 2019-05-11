import pygame
from src import display
from src import state_manager
from src.table import Table
from src.constants import *


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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_pressed[0]:
                if table.clicked_on_node():
                    table.node_pressed = True
                if not table.must_remove_piece:
                    if table.faze == FAZE2:
                        table.pick_up_piece()
                else:
                    if table.remove_opponent_piece():
                        morris.switch_state(GAME_STATE, control)
        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_pressed[0]:
                if table.faze == FAZE1:
                    if table.node_pressed:
                        if table.put_new_piece():
                            morris.switch_state(GAME_STATE, control)
                else:
                    if table.put_down_piece():
                        morris.switch_state(GAME_STATE, control)
            table.node_pressed = False

    table.update(mouse, mouse_pressed)


def run(control, *args):
    init()

    while morris.run:
        window.fill((180, 16, 180))
        update(control)
        render()
        morris.show_fps(window)
        pygame.display.flip()
        morris.tick()
