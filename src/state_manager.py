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

    @abstractmethod
    def on_exit(self):
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
        self.on_exit()

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
