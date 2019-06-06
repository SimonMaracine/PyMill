import pygame
from src import display
from src import state_manager
from src.table import Table
from src.button import TextButton
from src.constants import *
from src.states import pause


def init(*args):
    global table, buttons, server, client
    table = Table()
    button_font = pygame.font.SysFont("calibri", 36, True)
    button1 = TextButton(4, 16, "PAUSE", button_font, (255, 0, 0))
    buttons = (button1,)

    if args[0] == "host":
        pass
    elif args[0] == "client":
        pass


def render(surface):
    surface.fill((180, 16, 180))
    table.render(surface)
    for btn in buttons:
        btn.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            morris_ol.switch_state(EXIT, control)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_pressed[0]:
                if table.clicked_on_node():
                    table.node_pressed = True
                if not table.must_remove_piece:
                    if table.phase == PHASE2:
                        table.pick_up_piece()
            if any(map(lambda button: button.hovered(mouse), buttons)):
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_pressed[0]:
                if table.must_remove_piece:
                    if table.node_pressed:
                        if table.remove_opponent_piece():
                            morris_ol.switch_state(MORRIS_HOTSEAT_STATE, control)
                if table.phase == PHASE1:
                    if table.node_pressed:
                        if table.put_new_piece():
                            morris_ol.switch_state(MORRIS_HOTSEAT_STATE, control)
                else:
                    if table.put_down_piece():
                        morris_ol.switch_state(MORRIS_HOTSEAT_STATE, control)
            table.node_pressed = False

            if buttons[0].pressed(mouse, mouse_pressed):
                pause.run(control, display.window.copy())
            TextButton.button_down = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pause.run(control, display.window.copy())

    table.update(mouse, mouse_pressed)
    for btn in buttons:
        btn.update(mouse)


def run(control):
    global morris_ol
    morris_ol = state_manager.State(400, init, update, render, display.clock)
    morris_ol.show_fps = True
    morris_ol.run(control, display.window)