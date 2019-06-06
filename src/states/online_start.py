import socket
import pygame
from src import display
from src.display import WIDTH, HEIGHT
from src import state_manager
from src.button import Button, TextButton
from src.constants import *
from src.networking.client import Client
from src.networking.server import Server
from src.timer import Timer


def init():
    global buttons, host, client, timer_font, timer, mode
    timer_font = pygame.font.SysFont("calibri", 28, True)
    button_font = pygame.font.SysFont("calibri", 50, True)
    button1 = TextButton(120, 200, "HOST A GAME", button_font, (255, 0, 0))
    button2 = TextButton(120, 250, "CONNECT TO HOST", button_font, (255, 0, 0))
    button3 = TextButton(WIDTH // 2 + 200, HEIGHT - 80, "BACK", button_font, (255, 0, 0)).offset(0)
    button4 = TextButton(120, 320, "START GAME", button_font, (255, 0, 0))
    button4.lock()
    buttons = (button1, button2, button3, button4)

    ipv4_address = socket.gethostbyname(socket.gethostname())
    # print(ipv4_address)
    host = Server(ipv4_address, 5555)
    client = Client("192.168.56.1", 5555)
    mode = "host"
    timer = Timer(5)


def render(surface):
    surface.fill(BACKGROUND_COLOR)
    for btn in buttons:
        btn.render(surface)

    if host.waiting_for_conn:
        show_host_timer(surface)


def update(control):
    # global start_game
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
                if host.sock:
                    host.sock.close()
            elif buttons[3].pressed(mouse, mouse_pressed):
                if mode == "host":
                    online_start.switch_state(MORRIS_ONLINE_STATE, control, host)
                elif mode == "client":
                    online_start.switch_state(MORRIS_ONLINE_STATE, control, client)
                else:
                    print("There is no one to play with.")
            Button.button_down = False
            TextButton.button_down = False

    for btn in buttons:
        btn.update(mouse)

    if host.thread and timer.thread and not host.thread.is_alive() and not timer.thread.is_alive():
        buttons[0].unlock()
        buttons[1].unlock()

    if host.connection is not None or client.connected_to_server:
        buttons[3].unlock()
        buttons[0].lock()
        buttons[1].lock()

    # print("host: " + str(host.hosting))
    # print("client " + str(client))
    # if host.thread:
    #     print(host.thread.is_alive())
    # if timer.thread:
    #     print(timer.thread.is_alive())


def run(control):
    global online_start
    online_start = state_manager.State(600, init, update, render, display.clock)
    online_start.set_frame_rate(60)
    online_start.run(control, display.window)


def host_game():
    global host, mode
    mode = "host"
    host.run()
    timer.start()
    buttons[0].lock()
    buttons[1].lock()


def connect_to_host():
    global client, mode
    mode = "client"
    client.run()


def show_host_timer(surface):
    t = timer.get_time()
    text = timer_font.render("Waiting for connection... " + str(t), True, (0, 0, 0))
    surface.blit(text, (100, 420))
