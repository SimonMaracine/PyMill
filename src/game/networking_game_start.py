import socket
import tkinter as tk
from tkinter import messagebox
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

        frm_connect = tk.Frame(self, relief=tk.RIDGE, borderwidth=3, padx=26, pady=20)
        frm_connect.grid(row=1, column=0)

        self.frm_host = tk.Frame(self, relief=tk.RIDGE, borderwidth=3, padx=20, pady=20)
        self.frm_host.grid(row=1, column=1)

        tk.Label(frm_entries, text="IP").grid(row=0, column=0)
        tk.Label(frm_entries, text="Port").grid(row=1, column=0)

        self.ent_ip = tk.Entry(frm_entries, width=16)
        self.ent_port = tk.Entry(frm_entries, width=6)
        self.ent_ip.grid(row=0, column=1)
        self.ent_port.grid(row=1, column=1, sticky=tk.W)

        self.ent_port.insert(0, "5555")

        tk.Button(frm_connect, text="Connect", command=self.connect).grid(row=0, column=0)
        tk.Button(self.frm_host, text="Make New Game", command=self.host).grid(row=0, column=0)

        tk.Label(frm_connect, text="Connect to a game").grid(row=1, column=0)

        self.time = NetworkingGameStart.HOST_TIME
        self.var_time_countdown = tk.IntVar(self.frm_host, value=self.time)
        self.lbl_time = tk.Label(self.frm_host, text="0")
        self.lbl_time.grid(row=1, column=0)
        self.hosting = False

        lbl_your_ip_address = tk.Label(frm_your_ip_address, text="Your IP adddress:")
        lbl_your_ip_address.grid(row=0, column=0)

        self.ip = socket.gethostbyname(socket.gethostname())
        if self.ip[0:3] == "127":  # TODO check that this is always the case
            messagebox.showerror("No Internet", "You are not connected to the internet.", parent=self.top_level)

        lbl_ip = tk.Label(frm_your_ip_address, text=self.ip)
        lbl_ip.grid(row=1, column=0)

    def host(self):
        if not self.hosting:
            port = int(self.ent_port.get())

            if port < 1024:
                messagebox.showerror("Invalid Port", "Privileged ports (<1024) cannot be used.", parent=self.top_level)
                return
            if port > 65535:
                messagebox.showerror("Invalid Port", f"Port {port} doesn't exist.", parent=self.top_level)
                return

            try:
                server = Server(self.ip, port)  # Server just started
            except OSError as err:
                if str(err).find("Errno 98") != -1:
                    messagebox.showerror("Address Error", "This address is already in use. Pick another port.",
                                         parent=self.top_level)
                    return
            client = Client(0)  # FIXME the client and the server don't get garbage collected when pymill_network exits

            client.connect(self.ip, port)

            self.hosting = True

            self.check_both_clients_connected(server, client)
            self.time_countdown(server, client)

    def connect(self):
        ip = self.ent_ip.get()
        port = int(self.ent_port.get())

        client = Client(1)
        try:
            client.connect(ip, port)
        except ConnectionRefusedError:
            messagebox.showerror("Connect Error", "Could not find the server on that address.", parent=self.top_level)
            return

        self.exit()
        PyMillNetwork(tk.Toplevel(), self.on_game_exit, False, client)

    def check_both_clients_connected(self, server: Server, client: Client):
        if server.finished_listening:
            self.exit()
            PyMillNetwork(tk.Toplevel(), self.on_game_exit, True, client, server)
            self.hosting = False
        # This else fixes the method from calling itself forever
        else:
            if self.hosting:
                self.after(200, self.check_both_clients_connected, server, client)

    def time_countdown(self, server: Server, client: Client):
        # If the time was out, restart it
        if self.time == 0:
            self.time = NetworkingGameStart.HOST_TIME

        if self.time == NetworkingGameStart.HOST_TIME:
            self.lbl_time["textvariable"] = self.var_time_countdown

        self.time -= 1
        self.var_time_countdown.set(self.time)

        if self.time > 0:
            self.after(999, self.time_countdown, server, client)
            print("time countdown")
        else:
            self.time = 0
            self.lbl_time["text"] = 0

            # Clean up server and client
            self.hosting = False
            server.close()
            client.close()

    def exit(self):
        self.top_level.destroy()
        self.on_game_exit()
