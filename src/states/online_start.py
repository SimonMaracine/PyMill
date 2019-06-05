import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.button import Button, TextButton
from src.constants import *
import socket
from src.networking.client import Client
from src.networking.server import Server

host = None
client = None


def init():
    global buttons
    button_font = pygame.font.SysFont("calibri", 50, True)
    button1 = TextButton(200, 200, "HOST A GAME", button_font, (255, 0, 0))
    button2 = TextButton(200, 250, "CONNECT TO HOST", button_font, (255, 0, 0))
    button3 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
    button4 = TextButton(200, 320, "START GAME", button_font, (255, 0, 0))
    buttons = (button1, button2, button3, button4)


def render(surface):
    surface.fill(BACKGROUND_COLOR)
    for btn in buttons:
        btn.render(surface)


def update(control):
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            online_start.switch_state(EXIT, control)
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
                if host:
                    host.sock.close()
            elif buttons[3].pressed(mouse, mouse_pressed):
                if (host and host.connection is not None) or (client and client.connected_to_server):
                    online_start.switch_state(MORRIS_ONLINE_STATE, control, "host")
                else:
                    print("There is no one to play with.")
            Button.button_down = False
            TextButton.button_down = False

    for btn in buttons:
        btn.update(mouse)


def run(control):
    global online_start
    online_start = state_manager.State(600, init, update, render, display.clock)
    online_start.run(control, display.window)


def host_game():
    global host
    ipv4_address = socket.gethostbyname(socket.gethostname())
    print(ipv4_address)
    host = Server(ipv4_address, 5555)
    host.run()


def connect_to_host():
    global client
    client = Client("192.168.56.1", 5555)
    client.run()
