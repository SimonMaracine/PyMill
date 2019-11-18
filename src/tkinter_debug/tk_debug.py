import logging
import tkinter as tk
from typing import Callable

from src.log import get_logger

logger = get_logger(__name__)
logger.setLevel(logging.DEBUG)


class DebugWindow(tk.Frame):

    def __init__(self):
        self._top_level = tk.Toplevel()
        self._top_level.wm_minsize(100, 80)
        self._top_level.attributes("-topmost", True)
        self._position_window()

        self._top_level.bind("<ButtonPress-3>", self._start_move)
        self._top_level.bind("<ButtonRelease-3>", self._stop_move)
        self._top_level.bind("<B3-Motion>", self._on_motion)

        super().__init__(self._top_level)
        self.pack(padx=5, pady=5)

    def __del__(self):
        logger.debug("TK WINDOW DESTROYED AUTOMATICALLY")
        if tk.Toplevel.winfo_exists(self._top_level):  # TODO _tkinter.TclError: can't invoke "winfo" command: application has been destroyed
            self._top_level.destroy()

    def close(self):
        if tk.Toplevel.winfo_exists(self._top_level):
            self._top_level.destroy()

    def _start_move(self, event):
        self.x = event.x
        self.y = event.y + 30

    def _stop_move(self, event):
        self.x = None
        self.y = None

    def _on_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self._top_level.winfo_x() + deltax
        y = self._top_level.winfo_y() + deltay
        self._top_level.geometry("+%s+%s" % (x, y))

    def _position_window(self):
        width = _root.winfo_screenwidth()
        height = _root.winfo_screenheight()
        logger.debug(f"Display WIDTH-{width}, HEIGHT-{height}")
        x = width // 2 + 100
        y = height // 2 - 100
        self._top_level.geometry("+%s+%s" % (x, y))


def tk_init():
    global _root, _destroyed
    _root = tk.Tk()
    _root.wm_minsize(100, 80)
    _root.withdraw()


def tk_quit():
    global _destroyed
    _destroyed = True
    _root.destroy()


def update():
    if not _destroyed:
        _root.update()


_destroyed = False
_root = None
