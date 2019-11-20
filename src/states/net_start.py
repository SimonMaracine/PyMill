import configparser
import logging
from os.path import join
from typing import Tuple

import pygame

from src.display import WIDTH, HEIGHT
from src.gui.button import Button, TextButton
from src.gui.text_entry import TextEntry
from src.constants import *
from src.networking.client import Client
from src.networking.server import Server
from src.timer import Timer
from ..helpers import Boolean, serialize, deserialize
from ..gui.conn_status import ConnStatus
# from src.file_io import read_file
from src.log import get_logger
from src.networking.package import Package
from src.state_manager import State
from src.fonts import button_font

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


class NetStart(State):

    def __init__(self, id_, control):
        super().__init__(id_, control)

        button1 = TextButton(120, 50, "HOST A GAME", button_font, (255, 0, 0))
        button2 = TextButton(120, 100, "CONNECT TO HOST", button_font, (255, 0, 0))
        button3 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
        button4 = TextButton(120, 170, "READY", button_font, (255, 0, 0))
        button4.lock()
        self.buttons = (button1, button2, button3, button4)
        self.host_entry = TextEntry(120 + button2.width + 10, 100, 240, 15)

        port, ipv4_address = NetStart.get_port_and_ip()

        self.host = Server(ipv4_address, int(port))
        self.client = Client("", int(port))
        self.mode = 0
        self.started_game = Boolean(False)
        self.client_started = False
        self.host_started = False
        self.timer = Timer(61)
        self.conn = ConnStatus(120, 270, self.host, self.client)
        self.conn_established = False

        self.package = Package(self.started_game, None, Boolean(False))

    def on_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.switch_state(EXIT, self._control)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.host_entry.backspace()
                elif event.key == pygame.K_RETURN:
                    self.connect_to_host()
                else:
                    if event.unicode not in ("", "\x1b", "\t"):
                        self.host_entry.insert_character(event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if any(map(lambda button: button.hovered(event.pos), self.buttons)):
                    Button.button_down = True
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].pressed(event.pos, event.button):
                    self.host_game()
                elif self.buttons[1].pressed(event.pos, event.button):
                    if not self.conn_established:
                        self.connect_to_host()
                elif self.buttons[2].pressed(event.pos, event.button):
                    self.switch_state(START_STATE, self._control)
                    self.host.disconnect = True
                    self.client.disconnect = True
                    if self.host.sock is not None:
                        logger.debug("Trying to stop the listening socket")
                        try:
                            self.host.stop_sock()
                        except OSError as err:
                            print(err)
                elif self.buttons[3].pressed(event.pos, event.button):
                    if self.mode == HOST:
                        self.started_game.set(True)
                    elif self.mode == CLIENT:
                        self.started_game.set(True)
                if self.host_entry.pressed(event.pos, event.button):
                    self.host_entry.set_focus(True)
                else:
                    self.host_entry.set_focus(False)
                Button.button_down = False
                TextButton.button_down = False

    def update(self):
        mouse = pygame.mouse.get_pos()
        for btn in self.buttons:
            btn.update(mouse)

        if not self.host.waiting_for_conn and self.timer.thread and not self.timer.thread.is_alive() \
                and not self.host.hosting:
            self.buttons[0].unlock()
            self.buttons[1].unlock()
            self.host_entry.unlock()
            self.conn_established = False

        if self.client.connected:
            self.buttons[0].lock()
            self.buttons[1].lock()
            self.host_entry.lock()

        if self.host.hosting or self.client.connected:
            self.buttons[3].unlock()
            self.host_entry.unlock()

        # print("hosting: " + str(host.hosting))
        # if host.thread:
        #     print(host.thread.is_alive())
        # if timer.thread:
        #     print(timer.thread.is_alive())

        self.conn.update(self.host, self.client, self.host_started, self.client_started, self.mode, self.timer)
        self.host_entry.update()

        self.host.send(serialize(self.package))
        self.client.send(serialize(self.package))

        try:
            self.client_started = deserialize(self.host.receive()).started.get()
            self.host_started = deserialize(self.client.receive()).started.get()
        except EOFError as err:
            print(err)
        except AttributeError as err:
            print(err)

        if self.mode == HOST:
            if self.client_started and self.started_game.get():
                print("Starting game")
                self.switch_state(MORRIS_NET_STATE, self._control, False, HOST, self.host, self.client)
        elif self.mode == CLIENT:
            if self.host_started and self.started_game.get():
                print("Starting game")
                self.switch_state(MORRIS_NET_STATE, self._control, False, CLIENT, self.host, self.client)

    def render(self, surface):
        surface.fill(BACKGROUND_COLOR)
        for btn in self.buttons:
            btn.render(surface)
        self.conn.render(surface)
        self.host_entry.render(surface)

    def on_exit(self):
        pass

    def host_game(self):
        if self.conn_established:
            return
        elif not self.host.run():
            return
        self.mode = HOST
        self.timer.start()
        self.buttons[0].lock()
        self.buttons[1].lock()
        self.host_entry.lock()
        self.conn_established = True

    def connect_to_host(self):
        self.client.host = self.host_entry.get_text()
        if self.conn_established:
            return
        elif not self.client.host:
            print("IP address not inserted")
            return
        self.mode = CLIENT

        self.conn_established = True
        self.client.run()

    @staticmethod
    def get_port_and_ip() -> Tuple[str, str]:
        config = configparser.ConfigParser()
        config.read(join("data", "settings.ini"))
        logger.debug(config.sections())

        port = config.get("networking", "port")
        ipv4_address = config.get("networking", "host")
        return port, ipv4_address


def run(control):
    net_start = NetStart(NET_START_STATE, control)
    net_start.run()
