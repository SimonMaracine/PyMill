"""Main game module. It must be imported from the game folder and its main() executed."""

import pygame
from src.states import morris_hotseat, menu, start, options, exit, online_start, morris_online, netsettings
from src.constants import *

VERSION = "v0.2.0"
control = {"state": MENU_STATE, "running": True, "args": tuple()}


def main():
    print("PyMill " + VERSION, end="\n\n")
    pygame.init()

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
            morris_online.run(control)
        elif current_state == ONLINE_START:
            online_start.run(control)
        elif current_state == NETSETTINGS:
            netsettings.run(control)
        elif current_state == EXIT:
            exit.run(control)

    pygame.quit()
