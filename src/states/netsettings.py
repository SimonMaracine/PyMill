import socket
import configparser
from os.path import join

import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.gui.button import Button, TextButton
from src.gui.text_entry import TextEntry
from src.constants import *
from src.fonts import button_font
from src.state_manager import State


class Netsettings(State):

    def __init__(self):
        button1 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
        button2 = TextButton(WIDTH // 2 - 230, HEIGHT // 2 - 75, "PORT", button_font, (255, 0, 0))
        button3 = TextButton(WIDTH // 2 - 230, HEIGHT // 2 - 25, "HOST", button_font, (255, 0, 0))
        button4 = TextButton(WIDTH // 2 - 230, HEIGHT // 2 + 50, "RESET", button_font, (255, 0, 0))
        self.buttons = (button1, button2, button3, button4)
        self.port_entry = TextEntry(WIDTH // 2 - 100, HEIGHT // 2 - 75, 130, 5)
        self.host_entry = TextEntry(WIDTH // 2 - 100, HEIGHT // 2 - 25, 240, 15)

        config = configparser.ConfigParser()
        config.read(join("data", "settings.ini"))
        # print(config.sections())
        port = config.get("networking", "port")
        ipv4_address = config.get("networking", "host")

        self.port_entry.insert_text(port)
        self.host_entry.insert_text(ipv4_address)

    def render(self, surface):
        surface.fill(BACKGROUND_COLOR)
        for btn in self.buttons:
            btn.render(surface)

        self.port_entry.render(surface)
        self.host_entry.render(surface)

    def update(self, control):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                netsettings.switch_state(EXIT, control)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.port_entry.backspace()
                    self.host_entry.backspace()
                elif event.key == pygame.K_RETURN:
                    self.port_entry.set_focus(False)
                    self.host_entry.set_focus(False)
                else:
                    if event.unicode not in ("", "\x1b", "\t"):
                        self.port_entry.insert_character(event.unicode)
                        self.host_entry.insert_character(event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if any(map(lambda button: button.hovered(mouse), self.buttons)):
                    Button.button_down = True
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].pressed(mouse, mouse_pressed):
                    self.apply_changes()
                    netsettings.switch_state(OPTIONS_STATE, control)
                elif self.buttons[3].pressed(mouse, mouse_pressed):
                    ipv4_address = socket.gethostbyname(socket.gethostname())
                    # print(ipv4_address)
                    self.host_entry.insert_text(ipv4_address)
                    self.port_entry.insert_text("5555")
                if self.port_entry.pressed(mouse, mouse_pressed):
                    self.port_entry.set_focus(True)
                else:
                    self.port_entry.set_focus(False)
                if self.host_entry.pressed(mouse, mouse_pressed):
                    self.host_entry.set_focus(True)
                else:
                    self.host_entry.set_focus(False)
                Button.button_down = False
                TextButton.button_down = False

        self.buttons[0].update(mouse)
        self.buttons[3].update(mouse)

        self.port_entry.update()
        self.host_entry.update()

    def apply_changes(self):
        config = configparser.ConfigParser()
        config.read(join("data", "settings.ini"))

        port = self.port_entry.get_text()
        host = self.host_entry.get_text()
        config.set("networking", "port", port)
        config.set("networking", "host", host)

        with open(join("data", "settings.ini"), "w") as f:
            config.write(f)


def run(control):
    global netsettings
    netsettings = state_manager.State(NETSETTINGS_STATE, Netsettings(), display.clock)
    netsettings.run(control, display.window)
