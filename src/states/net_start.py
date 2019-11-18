import configparser
import logging
import tkinter as tk
from os.path import join

import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
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
from src.tkinter_debug import tk_debug
from src.state_manager import State

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


class NetStart(State):

    def __init__(self):
        # timer_font = pygame.font.SysFont("calibri", 28, True)
        button_font = pygame.font.SysFont("calibri", 50, True)
        button1 = TextButton(120, 50, "HOST A GAME", button_font, (255, 0, 0))
        button2 = TextButton(120, 100, "CONNECT TO HOST", button_font, (255, 0, 0))
        button3 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
        button4 = TextButton(120, 170, "READY", button_font, (255, 0, 0))
        button4.lock()
        self.buttons = (button1, button2, button3, button4)
        self.host_entry = TextEntry(120 + button2.width + 10, 100, 240, 15)

        config = configparser.ConfigParser()
        config.read(join("data", "settings.ini"))
        # print(config.sections())
        port = int(config.get("networking", "port"))
        ipv4_address = config.get("networking", "host")

        self.host = Server(ipv4_address, port)
        self.client = Client("", port)
        self.mode = int
        self.started_game = Boolean(False)
        self.client_started = False
        self.host_started = False
        self.timer = Timer(61)
        self.conn = ConnStatus(120, 270, self.host, self.client)

        self.package = Package(self.started_game, None, Boolean(False))

        self.frame = tk_debug.DebugWindow()
        self.slider = tk.Scale(self.frame)
        self.slider.pack()

    def render(self, surface):
        surface.fill(BACKGROUND_COLOR)
        for btn in self.buttons:
            btn.render(surface)
        self.conn.render(surface)
        self.host_entry.render(surface)

    def update(self, control):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                net_start.switch_state(EXIT, control)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.host_entry.backspace()
                elif event.key == pygame.K_RETURN:
                    self.connect_to_host()
                else:
                    if event.unicode not in ("", "\x1b", "\t"):
                        self.host_entry.insert_character(event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if any(map(lambda button: button.hovered(mouse), self.buttons)):
                    Button.button_down = True
                    TextButton.button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].pressed(mouse, mouse_pressed):
                    self.host_game()
                elif self.buttons[1].pressed(mouse, mouse_pressed):
                    self.connect_to_host()
                elif self.buttons[2].pressed(mouse, mouse_pressed):
                    net_start.switch_state(START_STATE, control)
                    self.host.disconnect = True
                    self.client.disconnect = True
                    if self.host.sock is not None:
                        logger.debug("Trying to stop the listening socket")
                        try:
                            self.host.stop_sock()
                        except OSError as e:
                            print(e)
                elif self.buttons[3].pressed(mouse, mouse_pressed):
                    if self.mode == HOST:
                        self.started_game.set(True)
                    elif self.mode == CLIENT:
                        self.started_game.set(True)
                if self.host_entry.pressed(mouse, mouse_pressed):
                    self.host_entry.set_focus(True)
                else:
                    self.host_entry.set_focus(False)
                Button.button_down = False
                TextButton.button_down = False

        for btn in self.buttons:
            btn.update(mouse)

        if not self.host.waiting_for_conn and self.timer.thread and not self.timer.thread.is_alive() \
                and not self.host.hosting:
            self.buttons[0].unlock()
            self.buttons[1].unlock()
            self.host_entry.unlock()

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
        except EOFError:
            pass
        except AttributeError as e:
            print(e)

        if self.mode == HOST:
            if self.client_started and self.started_game.get():
                print("Starting game")
                net_start.switch_state(MORRIS_NET_STATE, control, False, HOST, self.host, self.client)
        elif self.mode == CLIENT:
            if self.host_started and self.started_game.get():
                print("Starting game")
                net_start.switch_state(MORRIS_NET_STATE, control, False, CLIENT, self.host, self.client)

        tk_debug.update()

    def host_game(self):
        if not self.host.run():
            return
        self.mode = HOST
        self.timer.start()
        self.buttons[0].lock()
        self.buttons[1].lock()
        self.host_entry.lock()

    def connect_to_host(self):
        self.mode = CLIENT
        self.client.host = self.host_entry.get_text()
        if not self.client.host:
            print("IP address not inserted")
            return
        self.client.run()


def run(control):
    global net_start
    net_start = state_manager.NewState(600, NetStart(), display.clock)
    net_start.set_frame_rate(60)
    net_start.run(control, display.window)
