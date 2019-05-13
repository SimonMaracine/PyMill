import os
from src.states import morris_hotseat
from src.states import menu
from src.constants import *

control = {"state": MENU_STATE, "running": True}


def main():
    while control["running"]:
        current_state = control["state"]
        if current_state == MENU_STATE:
            menu.run(control)
        elif current_state == START_STATE:
            pass
        elif current_state == OPTIONS_STATE:
            pass
        elif current_state == MORRIS_HOTSEAT_STATE:
            morris_hotseat.run(control)
        elif current_state == MORRIS_ONLINE_STATE:
            pass
