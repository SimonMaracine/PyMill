import socket
import tkinter as tk
from typing import Callable

from src.networking.server import Server
from src.networking.client import Client
from src.game.pymill_network import PyMillNetwork


class NetworkingGameStart(tk.Frame):

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable):
        super().__init__(top_level)
        self.top_level = top_level
        self.on_game_exit = on_game_exit
        self.pack(padx=20, pady=20, expand=True)

        self.top_level.title("Start Networking Game")
        self.top_level.wm_protocol("WM_DELETE_WINDOW", self.exit)

        frm_entries = tk.Frame(self, pady=5)
        frm_entries.grid(row=0, column=0, columnspan=2)

        frm_connect = tk.Frame(self, relief=tk.RIDGE, borderwidth=3, padx=50, pady=20)
        frm_connect.grid(row=1, column=0)

        frm_host = tk.Frame(self, relief=tk.RIDGE, borderwidth=3, padx=20, pady=20)
        frm_host.grid(row=1, column=1)

        tk.Label(frm_entries, text="IP").grid(row=0, column=0)
        tk.Label(frm_entries, text="Port").grid(row=1, column=0)

        self.ent_ip = tk.Entry(frm_entries, width=11)
        self.ent_port = tk.Entry(frm_entries, width=5)
        self.ent_ip.grid(row=0, column=1)
        self.ent_port.grid(row=1, column=1, sticky=tk.W)

        self.ent_ip.insert(0, "127.0.0.1")
        self.ent_port.insert(0, "5555")

        tk.Button(frm_connect, text="Connect", command=self.connect).grid(row=0, column=0)
        tk.Button(frm_host, text="Make New Game", command=self.host).grid(row=0, column=0)

    def host(self):
        # ip = socket.gethostbyname(socket.gethostname())
        ip = "127.0.0.1"
        port = int(self.ent_port.get())

        server = Server(ip, port)  # Server just started
        client = Client(0)

        client.connect(ip, port)

        self.check_both_clients_connected(server, client)

    def connect(self):
        ip = self.ent_ip.get()
        port = int(self.ent_port.get())

        client = Client(1)
        client.connect(ip, port)

        PyMillNetwork(tk.Toplevel(), self.on_game_exit, client)
        self.exit()

    def check_both_clients_connected(self, server: Server, client: Client):
        if server.finished_listening:
            PyMillNetwork(tk.Toplevel(), self.on_game_exit, client, server)
            self.exit()
            print("SOMETHING IS WRONG")

        self.after(200, self.check_both_clients_connected, server, client)

    def exit(self):
        self.top_level.destroy()
        self.on_game_exit()
