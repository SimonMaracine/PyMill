import os
from src.states import morris_hotseat
from src.constants import *

control = {"state": GAME_STATE, "running": True}


def main():
    while control["running"]:
        current_state = control["state"]
        if current_state == START_STATE:
            pass
        elif current_state == GAME_STATE:
            morris_hotseat.run(control)
        elif current_state == OPTIONS_STATE:
            pass
