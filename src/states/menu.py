import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.button import Button
from src.constants import *


def init(*args):
    global menu, window, buttons
    menu = state_manager.State(1, display.clock)
    window = display.window
    button_font = pygame.font.SysFont("calibri", 50, True)
    button1 = Button(WIDTH//2, HEIGHT//2 - 75, "PLAY", button_font, (255, 0, 0)).offset(0)
    button2 = Button(WIDTH//2, HEIGHT//2 - 25, "OPTIONS", button_font, (255, 0, 0)).offset(0)
    button3 = Button(WIDTH//2, HEIGHT//2 + 25, "QUIT", button_font, (255, 0, 0)).offset(0)
    buttons = (button1, button2, button3)


def render():
    for btn in buttons:
        btn.render(window)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu.exit()
            control["running"] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttons[0].pressed(mouse, mouse_pressed):
                menu.switch_state(MORRIS_HOTSEAT_STATE, control)
            elif buttons[1].pressed(mouse, mouse_pressed):
                pass
            elif buttons[2].pressed(mouse, mouse_pressed):
                menu.exit()
                control["running"] = False
            Button.button_down = False

    for btn in buttons:
        btn.update(mouse)


def run(control, *args):
    init()

    while menu.run:
        window.fill((0, 0, 0))
        update(control)
        render()
        pygame.display.flip()
        menu.tick()
