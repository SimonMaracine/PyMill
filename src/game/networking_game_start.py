import socket
import tkinter as tk
from typing import Callable

from src.networking.server import Server
from src.networking.client import Client
from src.game.pymill_network import PyMillNetwork


class NetworkingGameStart(tk.Frame):

    HOST_TIME = 30

    def __init__(self, top_level: tk.Toplevel, on_game_exit: Callable):
        super().__init__(top_level)
        self.top_level = top_level
        self.on_game_exit = on_game_exit
        self.pack(padx=20, pady=20, expand=True)

        self.top_level.title("Start Networking Game")
        self.top_level.wm_protocol("WM_DELETE_WINDOW", self.exit)

        frm_entries = tk.Frame(self, pady=5)
        frm_entries.grid(row=0, column=0)

        frm_your_ip_address = tk.Frame(self)
        frm_your_ip_address.grid(row=0, column=1)

        frm_connect = tk.Frame(self, relief=tk.RIDGE, borderwidth=3, padx=50, pady=20)
        frm_connect.grid(row=1, column=0)

        self.frm_host = tk.Frame(self, relief=tk.RIDGE, borderwidth=3, padx=20, pady=20)
        self.frm_host.grid(row=1, column=1)

        tk.Label(frm_entries, text="IP").grid(row=0, column=0)
        tk.Label(frm_entries, text="Port").grid(row=1, column=0)

        self.ent_ip = tk.Entry(frm_entries, width=16)
        self.ent_port = tk.Entry(frm_entries, width=5)
        self.ent_ip.grid(row=0, column=1)
        self.ent_port.grid(row=1, column=1, sticky=tk.W)

        self.ent_ip.insert(0, "127.0.0.1")
        self.ent_port.insert(0, "5555")

        tk.Button(frm_connect, text="Connect", command=self.connect).grid(row=0, column=0)
        tk.Button(self.frm_host, text="Make New Game", command=self.host).grid(row=0, column=0)

        tk.Label(frm_connect, text="Connect to a game").grid(row=1, column=0)

        self.time = NetworkingGameStart.HOST_TIME
        self.var_time_countdown = tk.IntVar(self.frm_host, value=self.time)
        self.lbl_time = tk.Label(self.frm_host, text="0")
        self.lbl_time.grid(row=1, column=0)

        lbl_your_ip_address = tk.Label(frm_your_ip_address, text="Your IP adddress:")
        lbl_your_ip_address.grid(row=0, column=0)

        lbl_ip = tk.Label(frm_your_ip_address, text=socket.gethostbyname(socket.gethostname()))
        lbl_ip.grid(row=1, column=0)

    def host(self):
        ip = socket.gethostbyname(socket.gethostname())
        # ip = "127.0.0.1"
        port = int(self.ent_port.get())

        server = Server(ip, port)  # Server just started
        client = Client(0)

        client.connect(ip, port)

        self.check_both_clients_connected(server, client)
        self.time_countdown()

    def connect(self):
        ip = self.ent_ip.get()
        port = int(self.ent_port.get())

        client = Client(1)
        client.connect(ip, port)

        self.exit()
        PyMillNetwork(tk.Toplevel(), self.on_game_exit, False, client)

    def check_both_clients_connected(self, server: Server, client: Client):
        if server.finished_listening:
            self.exit()
            PyMillNetwork(tk.Toplevel(), self.on_game_exit, True, client, server)
        # This else fixes the method from calling itself forever
        else:
            self.after(200, self.check_both_clients_connected, server, client)

    def time_countdown(self):
        # If the time was out, restart it
        if self.time == 0:
            self.time = NetworkingGameStart.HOST_TIME

        if self.time == NetworkingGameStart.HOST_TIME:
            self.lbl_time["textvariable"] = self.var_time_countdown

        self.time -= 1
        self.var_time_countdown.set(self.time)

        if self.time > 0:
            self.after(999, self.time_countdown)
        else:
            self.time = 0
            self.lbl_time["text"] = 0  # TODO clean up the server and the client here

    def exit(self):
        self.top_level.destroy()
        self.on_game_exit()
