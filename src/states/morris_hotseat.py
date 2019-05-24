import pygame
from src import display
from src import state_manager
from src.table import Table
from src.button import Button
from src.constants import *


def init(*args):
    global morris, window, table, buttons
    morris = state_manager.State(4, display.clock)
    morris.set_frame_rate(60)
    window = display.window
    table = Table()
    button_font = pygame.font.SysFont("calibri", 36, True)
    button1 = Button(16, 16, "BACK", button_font, (255, 0, 0))
    buttons = (button1,)


def render():
    table.render(window)
    for btn in buttons:
        btn.render(window)


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
                    if table.phase == PHASE2:
                        table.pick_up_piece()
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_pressed[0]:
                if table.must_remove_piece:
                    if table.node_pressed:
                        if table.remove_opponent_piece():
                            morris.switch_state(MORRIS_HOTSEAT_STATE, control)
                if table.phase == PHASE1:
                    if table.node_pressed:
                        if table.put_new_piece():
                            morris.switch_state(MORRIS_HOTSEAT_STATE, control)
                else:
                    if table.put_down_piece():
                        morris.switch_state(MORRIS_HOTSEAT_STATE, control)
            table.node_pressed = False

            if buttons[0].pressed(mouse, mouse_pressed):
                morris.switch_state(MENU_STATE, control)

    table.update(mouse, mouse_pressed)
    for btn in buttons:
        btn.update(mouse)


def run(control, *args):
    init()

    while morris.run:
        window.fill((180, 16, 180))
        update(control)
        render()
        morris.show_fps(window)
        pygame.display.flip()
        morris.tick()
