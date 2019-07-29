import pygame
from src.constants import *
from src.fonts import connstatus_font


class ConnStatus:
    def __init__(self, x: int, y: int, host, client):
        self.x = x
        self.y = y
        self.host = host
        self.client = client
        self.width = 500
        self.height = 140
        self.host_started_game = False
        self.client_started_game = False
        self.mode = int
        self.timer = None

    def render(self, surface):
        pygame.draw.rect(surface, (16, 16, 16), (self.x, self.y, self.width, self.height), 7)

        if self.mode == HOST:
            if self.host.waiting_for_conn or self.host.hosting:
                self.show_connection_host(surface)
        elif self.mode == CLIENT:
            if self.client.connected:
                self.show_connection_client(surface)

        if self.host.waiting_for_conn:
            self.show_host_timer(surface)

    def update(self, host, client, host_started: bool, client_started: bool, mode, timer):
        self.host = host
        self.client = client
        self.mode = mode
        self.host_started_game = host_started
        self.client_started_game = client_started
        self.timer = timer

    def show_connection_host(self, surface):
        text1 = connstatus_font.render("Client is connected" if self.host.connection is not None else "",
                                       True, (0, 0, 0))
        text2 = connstatus_font.render("Client is ready to start the game: {}".format(self.client_started_game), True, (0, 0, 0))

        surface.blit(text1, (self.x + 15, self.y + 15))
        if self.host.hosting:
            surface.blit(text2, (self.x + 15, self.y + 65))

    def show_connection_client(self, surface):
        text1 = connstatus_font.render("Connected to host" if self.client.connected else "",
                                       True, (0, 0, 0))
        text2 = connstatus_font.render("Host is ready to start the game: {}".format(self.host_started_game), True, (0, 0, 0))

        surface.blit(text1, (self.x + 15, self.y + 15))
        surface.blit(text2, (self.x + 15, self.y + 65))

    def show_host_timer(self, surface):
        t = self.timer.get_time()
        text = connstatus_font.render("Waiting for connection... " + str(t), True, (0, 0, 0))
        surface.blit(text, (self.x + 15, self.y + 15))
