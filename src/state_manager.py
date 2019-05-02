import pygame
from src.display import HEIGHT


class State:
    def __init__(self, index, clock):
        self.index = index
        self.run = True
        self.clock = clock
        self.fps = 60
        self.fps_font = pygame.font.SysFont("calibri", 20, True)

    def exit(self):
        self.run = False

    def switch_state(self, to_state: int, control: dict):
        self.exit()
        control["state"] = to_state

    def set_frame_rate(self, fps):
        self.fps = fps

    def tick(self):
        self.clock.tick(self.fps)

    def show_fps(self, surface):
        text = self.fps_font.render("FPS: " + str(int(self.clock.get_fps())), True, (255, 255, 80))
        surface.blit(text, (8, HEIGHT - 23))
