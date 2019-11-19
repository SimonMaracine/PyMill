from src.state_manager import State


class Exit(State):

    def __init__(self, id_, control):
        super().__init__(id_, control)

    def on_event(self):
        pass

    def update(self):
        pass

    def render(self, surface):
        pass


def run(control):
    control.running = False
