import socket
import configparser
import logging
from os.path import join
from typing import Tuple

import pygame

from src.display import WIDTH, HEIGHT
from src.gui.button import Button, TextButton
from src.gui.text_entry import TextEntry
from src.constants import *
from src.fonts import button_font
from src.state_manager import State
from src.log import get_logger


logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


class NetSettings(State):

    def __init__(self, id_, control):
        super().__init__(id_, control)

        button1 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
        button2 = TextButton(WIDTH // 2 - 230, HEIGHT // 2 - 75, "PORT", button_font, (255, 0, 0))
        button3 = TextButton(WIDTH // 2 - 230, HEIGHT // 2 - 25, "HOST", button_font, (255, 0, 0))
        button4 = TextButton(WIDTH // 2 - 230, HEIGHT // 2 + 50, "RESET", button_font, (255, 0, 0))
        self.buttons = (button1, button2, button3, button4)
        self.port_entry = TextEntry(WIDTH // 2 - 100, HEIGHT // 2 - 75, 130, 5)
        self.host_entry = TextEntry(WIDTH // 2 - 100, HEIGHT // 2 - 25, 240, 15)

        port, ipv4_address = NetSettings.get_port_and_ip()
        self.port_entry.insert_text(port)
        self.host_entry.insert_text(ipv4_address)

    def on_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.switch_state(EXIT, self._control)
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
                if any(map(lambda button: button.hovered(event.pos), self.buttons)):
                    Button.button_down = True
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].pressed(event.pos, event.button):
                    self.apply_changes()
                    self.switch_state(OPTIONS_STATE, self._control)
                elif self.buttons[3].pressed(event.pos, event.button):
                    ipv4_address = socket.gethostbyname(socket.gethostname())
                    # print(ipv4_address)
                    self.host_entry.insert_text(ipv4_address)
                    self.port_entry.insert_text("5555")
                if self.port_entry.pressed(event.pos, event.button):
                    self.port_entry.set_focus(True)
                else:
                    self.port_entry.set_focus(False)
                if self.host_entry.pressed(event.pos, event.button):
                    self.host_entry.set_focus(True)
                else:
                    self.host_entry.set_focus(False)
                Button.button_down = False
                TextButton.button_down = False

    def update(self):
        mouse = pygame.mouse.get_pos()

        self.buttons[0].update(mouse)
        self.buttons[3].update(mouse)

        self.port_entry.update()
        self.host_entry.update()

    def render(self, surface):
        surface.fill(BACKGROUND_COLOR)
        for btn in self.buttons:
            btn.render(surface)

        self.port_entry.render(surface)
        self.host_entry.render(surface)

    def apply_changes(self):
        config = configparser.ConfigParser()
        config.read(join("data", "settings.ini"))

        port = self.port_entry.get_text()
        host = self.host_entry.get_text()
        config.set("networking", "port", port)
        config.set("networking", "host", host)

        with open(join("data", "settings.ini"), "w") as f:
            config.write(f)

    @staticmethod
    def get_port_and_ip() -> Tuple[str, str]:
        config = configparser.ConfigParser()
        config.read(join("data", "settings.ini"))
        logger.debug(config.sections())

        port = config.get("networking", "port")
        ipv4_address = config.get("networking", "host")
        return port, ipv4_address


def run(control):
    net_settings = NetSettings(NET_SETTINGS_STATE, control)
    net_settings.run()
