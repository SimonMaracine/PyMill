"""Main game module. It must be imported from the game folder and its main() executed."""

import pygame
from src.states import morris_hotseat, menu, start, options, exit, \
        net_start, morris_net_server, morris_net_client, net_settings, the_other_disconnected
from src.constants import *
from src.tkinter_debug import tk_debug
from src.state_manager import Control

VERSION = "v0.2.0"
control = Control(state=MENU_STATE, running=True, args=())


def main():
    print("PyMill " + VERSION, end="\n\n")
    pygame.init()
    tk_debug.tk_init()

    while control.running:
        current_state = control.state

        if current_state == MENU_STATE:
            menu.run(control)
        elif current_state == START_STATE:
            start.run(control)
        elif current_state == OPTIONS_STATE:
            options.run(control)
        elif current_state == MORRIS_HOTSEAT_STATE:
            morris_hotseat.run(control)
        elif current_state == MORRIS_NET_STATE_SERVER:
            morris_net_server.run(control)
        elif current_state == MORRIS_NET_STATE_CLIENT:
            morris_net_client.run(control)
        elif current_state == NET_START_STATE:
            net_start.run(control)
        elif current_state == NET_SETTINGS_STATE:
            net_settings.run(control)
        elif current_state == THE_OTHER_DISCONNECTED:
            the_other_disconnected.run(control)
        elif current_state == EXIT:
            exit.run(control)

    tk_debug.tk_quit()
    pygame.quit()
