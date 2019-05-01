class State:
    def __init__(self, index, clock):
        self.index = index
        self.run = True
        self.clock = clock
        self.fps = 60

    def exit(self):
        self.run = False

    def switch_state(self, to_state: int, control: dict):
        self.exit()
        control["state"] = to_state

    def set_frame_rate(self, fps):
        self.fps = fps

    def tick(self):
        self.clock.tick(self.fps)
