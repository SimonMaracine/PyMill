import tkinter as tk

from src.networking.server import Server
from src.networking.client import Client
from src.constants import *

ip = "127.0.0.1"

client1 = None
client2 = None


def host():
    global client1
    Server(ip, 5546)
    client1 = Client(0)
    client1.connect(ip, 5546)


def connect():
    global client2
    client2 = Client(1)
    client2.connect(ip, 5546)


def send_event():
    client1.send_event(PLACE_PIECE, 18)


def listen_events():
    message = client2.receive_event()
    if message.action == PLACE_PIECE:
        print("PLACE PIECE")
        print(message.args[0])
    elif message.action == MOVE_PIECE:
        print("MOVE PIECE")
    elif message.action == REMOVE_PIECE:
        print("REMOVE PIECE")
    elif message.action == CHANGE_TURN:
        print("CHANGE_TURN")
    elif message.action == CLOSE_CONNECTION:
        print("CLOSE CONNECTION REQUESTED")

    root.after(200, listen_events)


root = tk.Tk()

tk.Button(root, text="Host", command=host).pack()
tk.Button(root, text="Connect", command=connect).pack()
tk.Button(root, text="Send event", command=send_event).pack()
tk.Button(root, text="Start client2 listening for events", command=listen_events).pack()

root.mainloop()
