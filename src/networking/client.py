import socket
from ..helpers import create_thread, create_socket, serialize, Boolean


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connected = False
        self.disconnect = False
        self.sock = None
        # self.thread = None

        self.to_send: bytes = b"HEY!!!"
        self.to_be_received: bytes = serialize(Boolean(False))

    def prepare(self):
        self.sock = create_socket()
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
        except socket.gaierror:
            print("Invalid IP address")
            return False
        except ConnectionRefusedError:
            print("Could not connect to server")
            return False

    def server(self):
        with self.sock as sock:
            while not self.disconnect:
                try:
                    data: bytes = sock.recv(16384)
                    # try:
                    #     print("Received: {}".format(deserialize(data)))
                    # except EOFError:
                    #     pass
                    self.to_be_received = data

                    if not data:
                        print("Server sent nothing")
                        break

                    sock.send(self.to_send)
                    # print("Sent: {}".format(self.to_send))
                except ConnectionResetError:
                    print("Server has probably closed the connection")
                    break
                # except ConnectionError:
                #     print("An unexpected error occurred")
                #     break

        self.connected = False
        print("Disconnected from server")

    def send(self, data: bytes):
        self.to_send = data

    def receive(self) -> bytes:
        return self.to_be_received
