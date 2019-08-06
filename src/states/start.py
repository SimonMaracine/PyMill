import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.gui.button import Button, TextButton
from src.constants import *
from src.fonts import button_font


def init():
    global buttons
    button1 = Button(110, 100, 250, 300)
    button2 = Button(430, 100, 250, 300)
    button3 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
    buttons = (button1, button2, button3)


def render(surface):
    surface.fill(BACKGROUND_COLOR)
    for btn in buttons:
        btn.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start.switch_state(EXIT, control)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttons[0].pressed(mouse, mouse_pressed):
                start.switch_state(MORRIS_HOTSEAT_STATE, control)
            elif buttons[1].pressed(mouse, mouse_pressed):
                start.switch_state(ONLINE_START_STATE, control)
            elif buttons[2].pressed(mouse, mouse_pressed):
                start.switch_state(MENU_STATE, control)
            Button.button_down = False
            TextButton.button_down = False

    for btn in buttons:
        btn.update(mouse)


def run(control):
    global start
    start = state_manager.State(START_STATE, init, update, render, display.clock)
    start.run(control, display.window)
