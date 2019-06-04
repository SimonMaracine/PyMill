import os
from src.states import morris_hotseat, menu, start, options, exit, online_start, morris_online
from src.constants import *

control = {"state": MENU_STATE, "running": True}


def main():
    while control["running"]:
        current_state = control["state"]
        if current_state == MENU_STATE:
            menu.run(control)
        elif current_state == START_STATE:
            start.run(control)
        elif current_state == OPTIONS_STATE:
            options.run(control)
        elif current_state == MORRIS_HOTSEAT_STATE:
            morris_hotseat.run(control)
        elif current_state == MORRIS_ONLINE_STATE:
            pass
        elif current_state == ONLINE_START:
            online_start.run(control)
        elif current_state == EXIT:
            exit.run(control)
