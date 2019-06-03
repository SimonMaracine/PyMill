import pygame
from src.display import HEIGHT, window


class State:
    def __init__(self, index: int, init, update, render, clock):
        self.index = index
        self._init = init
        self._update = update
        self._render = render
        self._clock = clock
        self._running = True
        self._fps = 60
        self.fps_font = pygame.font.SysFont("calibri", 18, True)

        self._mouse = ()
        self._mouse_pressed = ()

    def run(self, control, surface):
        self._init()
        while self._running:
            self._mouse = pygame.mouse.get_pos()
            self._mouse_pressed = pygame.mouse.get_pressed()
            window.fill((0, 0, 0))
            self._update(control)
            self._render(surface)
            pygame.display.flip()
            self.tick()

    def exit(self):
        self._running = False

    def switch_state(self, to_state: int, control: dict):
        self.exit()
        control["state"] = to_state

    def set_frame_rate(self, fps):
        self._fps = fps

    def tick(self):
        self._clock.tick(self._fps)

    def show_fps(self, surface):
        text = self.fps_font.render("FPS: " + str(int(self._clock.get_fps())), True, (255, 255, 16))
        surface.blit(text, (7, HEIGHT - 22))

    def get_mouse(self):
        return self._mouse

    def get_mouse_pressed(self):
        return self._mouse_pressed
