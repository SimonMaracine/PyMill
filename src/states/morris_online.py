import time
import configparser
import pygame
from src import display
from src import state_manager
from src.game_objects.table import Table
from src.gui.button import TextButton
from src.constants import *
from src.states import pause
from ..helpers import serialize, deserialize, str_to_tuple


def init(*args):
    global table, buttons, mode, host, client, turn, change_turn, bg_color
    mode = args[0]
    host = args[1]
    client = args[2]
    turn = CLIENT
    change_turn = False

    if mode == HOST:
        table = Table()
        host.send(serialize((table, change_turn)))
        time.sleep(0.3)
    else:
        table = Table()
        client.send(serialize((table, change_turn)))

    button_font = pygame.font.SysFont("calibri", 36, True)
    button1 = TextButton(4, 16, "PAUSE", button_font, (255, 0, 0))
    buttons = (button1,)

    config = configparser.ConfigParser()
    config.read("data\\settings.ini")
    bg_color = config.get("theme", "bgcolor")
    bg_color = str_to_tuple(bg_color)


def render(surface):
    surface.fill(bg_color)
    table.render(surface)
    for btn in buttons:
        btn.render(surface)


def update(control):
    global table, turn, change_turn
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    if mode == turn:
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
                            table.remove_opponent_piece()
                            change_turn = True
                    if table.phase == PHASE1:
                        if table.node_pressed:
                            table.put_new_piece()
                            change_turn = True
                    else:
                        table.put_down_piece()
                        change_turn = True
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

        if table.game_over:
            morris_ol.switch_state(MORRIS_HOTSEAT_STATE, control)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                morris_ol.switch_state(EXIT, control)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if any(map(lambda button: button.hovered(mouse), buttons)):
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if buttons[0].pressed(mouse, mouse_pressed):
                    pause.run(control, display.window.copy())
                TextButton.button_down = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pause.run(control, display.window.copy())

        for btn in buttons:
            btn.update(mouse)

    if mode == HOST:
        if turn != mode:
            table, change_turn = deserialize(host.receive())
        else:
            host.send(serialize((table, change_turn)))
            if change_turn:
                time.sleep(0.1)
    else:
        if turn != mode:
            table, change_turn = deserialize(client.receive())
        else:
            client.send(serialize((table, change_turn)))
            if change_turn:
                time.sleep(0.1)

    if change_turn:
        turn = switch_turn()
        change_turn = False

    print("HOST" if turn == HOST else "CLIENT")


def run(control):
    global morris_ol
    morris_ol = state_manager.State(400, init, update, render, display.clock)
    morris_ol.show_fps = True
    morris_ol.set_frame_rate(48)
    morris_ol.run(control, display.window)


def switch_turn() -> int:
    if turn == HOST:
        return CLIENT
    else:
        return HOST
