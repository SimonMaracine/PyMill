import tkinter as tk
from typing import Callable


class NetworkingGameStart(tk.Frame):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable):
        super().__init__(top_level)
        self.top_level = top_level
        self.on_game_exit = on_game_exit
        self.pack(padx=20, pady=20, expand=True)

        self.top_level.title("Start Networking Game")
        self.top_level.wm_protocol("WM_DELETE_WINDOW", self.exit)

        frm_entries = tk.Frame(self)
        frm_entries.grid(row=0, column=0, columnspan=2)

        frm_connect = tk.Frame(self, relief=tk.RIDGE, borderwidth=3, padx=50, pady=20)
        frm_connect.grid(row=1, column=0)

        frm_host = tk.Frame(self, relief=tk.RIDGE, borderwidth=3, padx=20, pady=20)
        frm_host.grid(row=1, column=1)

        tk.Label(frm_entries, text="IP").grid(row=0, column=0)
        tk.Label(frm_entries, text="Port").grid(row=1, column=0)

        ent_ip = tk.Entry(frm_entries, width=11)
        ent_port = tk.Entry(frm_entries, width=5)
        ent_ip.grid(row=0, column=1)
        ent_port.grid(row=1, column=1, sticky=tk.W)

        tk.Button(frm_connect, text="Connect", command=None).grid(row=0, column=0)
        tk.Button(frm_host, text="Make New Game", command=None).grid(row=0, column=0)

    def host(self):
        pass

    def connect(self):
        pass

    def exit(self):
        self.top_level.destroy()
        self.on_game_exit()
