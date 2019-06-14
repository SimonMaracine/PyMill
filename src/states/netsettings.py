import socket
import configparser
import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.gui.button import Button, TextButton
from src.gui.text_entry import TextEntry
from src.constants import *


def init():
    global buttons, port_entry, host_entry
    button_font = pygame.font.SysFont("calibri", 50, True)
    button1 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
    button2 = TextButton(WIDTH // 2 - 230, HEIGHT // 2 - 75, "PORT", button_font, (255, 0, 0))
    button3 = TextButton(WIDTH // 2 - 230, HEIGHT // 2 - 25, "HOST", button_font, (255, 0, 0))
    button4 = TextButton(WIDTH // 2 - 230, HEIGHT // 2 + 50, "RESET", button_font, (255, 0, 0))
    buttons = (button1, button2, button3, button4)
    port_entry = TextEntry(WIDTH // 2 - 100, HEIGHT // 2 - 75, 130, 5)
    host_entry = TextEntry(WIDTH // 2 - 100, HEIGHT // 2 - 25, 240, 15)

    config = configparser.ConfigParser()
    config.read("data\\settings.ini")
    # print(config.sections())
    port = config.get("networking", "port")
    ipv4_address = config.get("networking", "host")

    port_entry.insert_text(port)
    host_entry.insert_text(ipv4_address)


def render(surface):
    surface.fill(BACKGROUND_COLOR)
    for btn in buttons:
        btn.render(surface)

    port_entry.render(surface)
    host_entry.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            netsettings.switch_state(EXIT, control)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                port_entry.backspace()
                host_entry.backspace()
            elif event.key == pygame.K_RETURN:
                port_entry.set_focus(False)
                host_entry.set_focus(False)
            else:
                if event.unicode not in ("", "\x1b", "\t"):
                    port_entry.insert_character(event.unicode)
                    host_entry.insert_character(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttons[0].pressed(mouse, mouse_pressed):
                apply_changes()
                netsettings.switch_state(OPTIONS_STATE, control)
            elif buttons[3].pressed(mouse, mouse_pressed):
                ipv4_address = socket.gethostbyname(socket.gethostname())
                # print(ipv4_address)
                host_entry.insert_text(ipv4_address)
                port_entry.insert_text("5555")
            if port_entry.pressed(mouse, mouse_pressed):
                port_entry.set_focus(True)
            else:
                port_entry.set_focus(False)
            if host_entry.pressed(mouse, mouse_pressed):
                host_entry.set_focus(True)
            else:
                host_entry.set_focus(False)
            Button.button_down = False
            TextButton.button_down = False

    buttons[0].update(mouse)
    buttons[3].update(mouse)

    port_entry.update()
    host_entry.update()


def run(control):
    global netsettings
    netsettings = state_manager.State(700, init, update, render, display.clock)
    netsettings.run(control, display.window)


def apply_changes():
    config = configparser.ConfigParser()
    config.read("data\\settings.ini")

    port = port_entry.get_text()
    host = host_entry.get_text()
    config.set("networking", "port", port)
    config.set("networking", "host", host)

    with open("data\\settings.ini", "w") as f:
        config.write(f)
