import os
from src.states_id import *
from src.states import morris

control = {"state": GAME_STATE, "running": True}


def main():
    while control["running"]:
        current_state = control["state"]
        if current_state == START_STATE:
            pass
        elif current_state == GAME_STATE:
            morris.run(control)
        elif current_state == OPTIONS_STATE:
            pass
