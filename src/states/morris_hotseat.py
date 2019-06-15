import configparser
import pygame
from src import display
from src import state_manager
from src.game_objects.board import Board
from src.gui.button import TextButton
from src.constants import *
from src.states import pause
from src.helpers import str_to_tuple


def init():
    global board, buttons, bg_color
    board = Board()
    button_font = pygame.font.SysFont("calibri", 36, True)
    button1 = TextButton(4, 16, "PAUSE", button_font, (255, 0, 0))
    buttons = (button1,)

    config = configparser.ConfigParser()
    config.read("data\\settings.ini")
    bg_color = config.get("theme", "bgcolor")
    bg_color = str_to_tuple(bg_color)  # todo make fallback color


def render(surface):
    surface.fill(bg_color)
    board.render(surface)
    for btn in buttons:
        btn.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            morris.switch_state(EXIT, control)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_pressed[0]:
                if board.clicked_on_node():
                    board.node_pressed = True
                if not board.must_remove_piece:
                    if board.phase == PHASE2:
                        board.pick_up_piece()
            if any(map(lambda button: button.hovered(mouse), buttons)):
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if mouse_pressed[0]:
                if board.must_remove_piece:
                    if board.node_pressed:
                        board.remove_opponent_piece()
                if board.phase == PHASE1:
                    if board.node_pressed:
                        board.put_new_piece()
                else:
                    board.put_down_piece()
            board.node_pressed = False

            if buttons[0].pressed(mouse, mouse_pressed):
                pause.run(control, display.window.copy())
            TextButton.button_down = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pause.run(control, display.window.copy())

    board.update(mouse, mouse_pressed)
    for btn in buttons:
        btn.update(mouse)

    if board.game_over:
        morris.switch_state(MORRIS_HOTSEAT_STATE, control)


def run(control):
    global morris
    morris = state_manager.State(400, init, update, render, display.clock)
    morris.show_fps = True
    morris.run(control, display.window)
