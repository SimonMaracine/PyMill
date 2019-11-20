import socket
from typing import Callable

import pygame

from ..helpers import create_thread, create_socket, serialize, Boolean
from src.networking.package import Package


class Client:
    """Class representing a client object. It communicates with a Server object."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connected = False
        self.disconnect = False
        self.sock = None
        self.clock = pygame.time.Clock()

        self.to_send: bytes = b"HEY!!!"
        self.to_be_received: bytes = serialize(Package(Boolean(False), None, Boolean(False)))

        self._on_disconnect: Callable = lambda: None

    def prepare(self):
        self.sock = create_socket()
        self.sock.settimeout(10)
        if self.connect():
            self.connected = True

    def run(self):
        self.prepare()
        if self.connected:
            create_thread(target=self.server).start()

    def connect(self) -> bool:
        """Connects the client to a server.

        Returns:
            bool: True if connection succeeded, False otherwise.

        """
        print("Connecting to ({}, {})".format(self.host, self.port))
        try:
            self.sock.connect((self.host, self.port))
            print("Connected to server")
            return True
        except socket.gaierror as e:
            # print("Invalid IP address")
            print(e)
            return False
        except ConnectionRefusedError as e:
            # print("Could not connect to server")
            print(e)
            return False
        except (socket.timeout, TimeoutError) as e:
            # print("Connection attempt failed (timeout)")
            print(e)
            return False

    def server(self):
        """The send-receive loop with the server."""
        with self.sock as sock:
            while not self.disconnect:
                print("Client working")
                try:
                    data: bytes = sock.recv(16384)
                    # try:
                    #     print("Received: {}".format(deserialize(data)))
                    # except EOFError:
                    #     pass
                    self.to_be_received = data

                    if not data:
                        print("Server sent nothing")
                        self.disconnect = True

                    sock.send(self.to_send)
                    # print("Sent: {}".format(self.to_send))
                except ConnectionResetError as err:
                    # print("Server has probably closed the connection")
                    print(err)
                    self.disconnect = True
                except ConnectionAbortedError as err:
                    print(err)
                    self.disconnect = True
                except ConnectionError as err:
                    print(err)
                    self.disconnect = True

                self.clock.tick(40)

        self.connected = False
        self._on_disconnect()
        print("Disconnected from server")

    def send(self, data: bytes):
        self.to_send = data

    def receive(self) -> bytes:
        return self.to_be_received

    def set_on_disconnect(self, func: Callable):
        self._on_disconnect = func
