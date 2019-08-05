import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.gui.button import Button, TextButton
from src.constants import *


def init():
    global buttons, background
    button_font = pygame.font.SysFont("calibri", 50, True)
    button1 = TextButton(WIDTH // 2, HEIGHT // 2 - 75, "OPTIONS", button_font, (255, 0, 0)).offset(0)
    button2 = TextButton(WIDTH // 2, HEIGHT // 2 - 25, "EXIT TO MENU", button_font, (255, 0, 0)).offset(0)
    button3 = TextButton(WIDTH // 2, HEIGHT // 2 + 25, "BACK", button_font, (255, 0, 0)).offset(0)
    buttons = (button1, button2, button3)
    background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    background.fill(BACKGROUND_COLOR)


def render(surface):
    surface.blit(last_frame, (0, 0))
    surface.blit(background, (WIDTH // 4, HEIGHT // 4))
    for btn in buttons:
        btn.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pause.switch_state(EXIT, control)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttons[0].pressed(mouse, mouse_pressed):
                pass
            elif buttons[1].pressed(mouse, mouse_pressed):
                pause.switch_state(MENU_STATE, control)
            elif buttons[2].pressed(mouse, mouse_pressed):
                pause.exit()
            Button.button_down = False
            TextButton.button_down = False

    for btn in buttons:
        btn.update(mouse)


def run(control, *args):
    global pause, last_frame
    last_frame = args[0]
    pause = state_manager.State(PAUSE_STATE, init, update, render, display.clock)
    pause.run(control, display.window)
