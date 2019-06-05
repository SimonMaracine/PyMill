import pygame
from src.display import HEIGHT, window

states = []


class State:
    def __init__(self, id_: int, init, update, render, clock):
        self._id = id_
        self._init = init
        self._update = update
        self._render = render
        self._clock = clock
        self._running = True
        self._fps = 60
        self.show_fps = False
        self.fps_font = pygame.font.SysFont("calibri", 18, True)
        states.append(self)

    def run(self, control, surface):
        self._init(*control["args"])
        control["args"] = tuple()
        while self._running:
            self._update(control)
            window.fill((0, 0, 0))
            self._render(surface)
            if self.show_fps:
                self._show_fps(surface)
            pygame.display.flip()
            self.tick()

    def exit(self):
        self._running = False
        states.remove(self)

    def switch_state(self, to_state: int, control: dict, *args):
        for state in states:
            if state.get_id() != to_state and state.get_id() != self.get_id():
                state.exit()
        self.exit()
        control["state"] = to_state
        control["args"] = args

    def set_frame_rate(self, fps):
        self._fps = fps

    def tick(self):
        self._clock.tick(self._fps)

    def _show_fps(self, surface):
        text = self.fps_font.render("FPS: " + str(int(self._clock.get_fps())), True, (255, 255, 16))
        surface.blit(text, (7, HEIGHT - 22))

    def get_id(self):
        return self._id
