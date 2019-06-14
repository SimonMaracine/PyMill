import socket
import configparser
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
from src.clipboard import get_clipboard


def init():
    global buttons, host, client, timer_font, timer, mode, started_game, client_started, host_started, conn, host_entry
    timer_font = pygame.font.SysFont("calibri", 28, True)
    button_font = pygame.font.SysFont("calibri", 50, True)
    button1 = TextButton(120, 50, "HOST A GAME", button_font, (255, 0, 0))
    button2 = TextButton(120, 100, "CONNECT TO HOST", button_font, (255, 0, 0))
    button3 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
    button4 = TextButton(120, 170, "START GAME", button_font, (255, 0, 0))
    button4.lock()
    buttons = (button1, button2, button3, button4)
    host_entry = TextEntry(120 + button2.width + 10, 100, 240, 15)

    config = configparser.ConfigParser()
    config.read("data\\settings.ini")
    # print(config.sections())
    port = int(config.get("networking", "port"))
    ipv4_address = config.get("networking", "host")

    host = Server(ipv4_address, port)
    client = Client("", port)
    mode = int
    started_game = Boolean(False)
    client_started = False
    host_started = False
    timer = Timer(61)
    conn = ConnStatus(120, 270, host, client)


def render(surface):
    surface.fill(BACKGROUND_COLOR)
    for btn in buttons:
        btn.render(surface)
    conn.render(surface)
    host_entry.render(surface)


def update(control):
    global started_game, client_started, host_started, host_entry
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            online_start.switch_state(EXIT, control)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                host_entry.backspace()
            elif event.key == pygame.K_RETURN:
                connect_to_host()
            else:
                if event.unicode not in ("", "\x1b", "\t"):
                    host_entry.insert_character(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if any(map(lambda button: button.hovered(mouse), buttons)):
                Button.button_down = True
                TextButton.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttons[0].pressed(mouse, mouse_pressed):
                host_game()
            elif buttons[1].pressed(mouse, mouse_pressed):
                connect_to_host()
            elif buttons[2].pressed(mouse, mouse_pressed):
                online_start.switch_state(START_STATE, control)
                host.disconnect = True
                client.disconnect = True
                if host.sock:
                    host.sock.close()
            elif buttons[3].pressed(mouse, mouse_pressed):
                if mode == HOST:
                    started_game.set(True)
                elif mode == CLIENT:
                    started_game.set(True)
            if host_entry.pressed(mouse, mouse_pressed):
                host_entry.set_focus(True)
            else:
                host_entry.set_focus(False)
            Button.button_down = False
            TextButton.button_down = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                text = get_clipboard()
                host_entry.text = list(text)

    for btn in buttons:
        btn.update(mouse)

    if not host.waiting_for_conn and timer.thread and not timer.thread.is_alive() \
            and not host.hosting:
        buttons[0].unlock()
        buttons[1].unlock()
        host_entry.unlock()

    if client.connected:
        buttons[0].lock()
        buttons[1].lock()
        host_entry.lock()

    if host.hosting or client.connected:
        buttons[3].unlock()
        host_entry.unlock()

    # print("hosting: " + str(host.hosting))
    # if host.thread:
    #     print(host.thread.is_alive())
    # if timer.thread:
    #     print(timer.thread.is_alive())

    conn.update(host, client, host_started, client_started, mode, timer)
    host_entry.update(mouse, mouse_pressed)

    host.send(serialize(started_game))
    client.send(serialize(started_game))

    try:
        client_started = deserialize(host.receive()).get()
        host_started = deserialize(client.receive()).get()
    except EOFError:
        pass

    if mode == HOST:
        if client_started and started_game.get():
            print("Starting game")
            online_start.switch_state(MORRIS_ONLINE_STATE, control, HOST, host, client)
    elif mode == CLIENT:
        if host_started and started_game.get():
            print("Starting game")
            online_start.switch_state(MORRIS_ONLINE_STATE, control, CLIENT, host, client)


def run(control):
    global online_start
    online_start = state_manager.State(600, init, update, render, display.clock)
    online_start.set_frame_rate(60)
    online_start.run(control, display.window)


def host_game():
    global host, mode
    mode = HOST
    host.run()
    timer.start()
    buttons[0].lock()
    buttons[1].lock()
    host_entry.lock()


def connect_to_host():
    global client, mode, host_entry
    mode = CLIENT
    # host_entry.text = ["7", "1", "2", ".", ".", "4", "6", ".", "0", "."]
    client.host = host_entry.get_text()
    if not client.host:
        print("IP address not inserted")
        return
    client.run()
