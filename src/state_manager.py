from abc import ABC, abstractmethod
from dataclasses import dataclass

import pygame
from src.display import window, clock

states = []


@dataclass
class Control:
    state: int
    running: bool
    args: tuple


class State(ABC):

    def __init__(self, id_: int, control: Control):
        self._control = control
        self._id = id_
        self._running = True
        states.append(self)

    def __del__(self):
        print("DELETED A STATE")

    @abstractmethod
    def on_event(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface):
        pass

    def run(self):
        while self._running:
            self.on_event()
            self.update()
            window.fill((0, 0, 0))
            self.render(window)
            pygame.display.flip()
            clock.tick(30)

    def exit(self):
        self._running = False
        states.remove(self)

    def switch_state(self, to_state: int, control: Control, except_self=False, *args):
        for state in states:
            if state.get_id() != to_state or except_self:
                if state.get_id() != self.get_id():
                    state.exit()
        self.exit()
        control.state = to_state
        control.args = args

    def get_id(self):
        return self._id


# class NewState:
#     """Class representing a game state."""
#
#     def __init__(self, id_: int, state: State, clock: pygame.time.Clock):
#         self._id = id_
#         self._state = state
#         self._clock = clock
#         self._running = True
#         self._fps = 30
#         self.show_fps = False
#         states.append(self)
#
#     def run(self, control: Control, surface: pygame.Surface):
#         # self._state = self._state.__class__(*control["args"])
#         control.args = tuple()
#         while self._running:
#             self._state.update()  # TODO a lot to change here
#             window.fill((0, 0, 0))
#             self._state.render(surface)
#             if self.show_fps:
#                 self._show_fps(surface)
#             pygame.display.flip()
#             self._tick()
#
#     def exit(self):
#         self._running = False
#         states.remove(self)
#
#     def switch_state(self, to_state: int, control: Control, except_self=False, *args):
#         for state in states:
#             if state.get_id() != to_state or except_self:
#                 if state.get_id() != self.get_id():
#                     state.exit()
#         self.exit()
#         control.state = to_state
#         control.args = args
#
#     def set_frame_rate(self, fps: int):
#         self._fps = fps
#
#     def get_id(self):
#         return self._id
#
#     def _tick(self):
#         self._clock.tick(self._fps)
#
#     def _show_fps(self, surface: pygame.Surface):
#         text = fps_font.render("FPS: " + str(round(self._clock.get_fps())), True, (255, 255, 16))
#         surface.blit(text, (7, HEIGHT - 22))
