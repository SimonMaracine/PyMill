import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.gui.button import Button, TextButton
from src.constants import *
from src.fonts import button_font, title_font


def init():
    global buttons, background, who_won
    button1 = TextButton(WIDTH // 2, HEIGHT // 2, "PLAY AGAIN", button_font, (255, 0, 0)).offset(0)
    button2 = TextButton(WIDTH // 2, HEIGHT // 2 + 50, "EXIT TO MENU", button_font, (255, 0, 0)).offset(0)
    buttons = (button1, button2)
    background = pygame.Surface((WIDTH // 2, HEIGHT // 2))
    background.fill(BACKGROUND_COLOR)
    who_won = title_font.render(f"{'White' if winner == WHITE else 'Black'} won!", True, (0, 0, 0))
    print(winner)


def render(surface):
    surface.blit(last_frame, (0, 0))
    surface.blit(background, (WIDTH // 4, HEIGHT // 4))
    surface.blit(who_won, (WIDTH // 2 - who_won.get_width() // 2, HEIGHT // 2 - 90))
    for btn in buttons:
        btn.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over.switch_state(EXIT, control)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttons[0].pressed(mouse, mouse_pressed):
                game_over.switch_state(MORRIS_HOTSEAT_STATE, control, except_self=True)
            elif buttons[1].pressed(mouse, mouse_pressed):
                game_over.switch_state(MENU_STATE, control)
            Button.button_down = False
            TextButton.button_down = False

    for btn in buttons:
        btn.update(mouse)


def run(control, *args):
    global game_over, last_frame, winner
    last_frame = args[0]
    winner = args[1]
    game_over = state_manager.State(GAME_OVER_STATE, init, update, render, display.clock)
    game_over.run(control, display.window)
