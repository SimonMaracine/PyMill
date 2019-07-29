import socket
from ..helpers import create_thread, create_socket, Boolean, serialize


class Server:
    """Class representing a server object. It communicates with a Client object."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connection = None
        self.waiting_for_conn = False
        self.disconnect = False
        self.hosting = False
        self.sock = None
        self.thread = None

        self.to_send: bytes = b"Hallo!"
        self.to_be_received: bytes = serialize(Boolean(False))

    def prepare(self):
        self.sock = create_socket()
        self.bind()
        self.sock.settimeout(61)
        self.sock.listen(3)
        print("Server started. Waiting for connection...\n")

    def run(self):
        if not self.waiting_for_conn or self.hosting:
            self.prepare()
            self.thread = create_thread(target=self.wait_for_conns)
            self.thread.start()
            self.waiting_for_conn = True
        else:
            print("Server already running")

    def wait_for_conns(self):
        try:
            connection, address = self.sock.accept()
            print("Connected by {}".format(address))
        except OSError:
            connection = None
        except socket.timeout:
            print("Socket timed out")
            connection = None

        self.connection = connection

        if connection is not None:
            create_thread(target=self.client).start()
            self.hosting = True
        else:
            print("No connection returned")

        self.waiting_for_conn = False
        self.sock.close()
        print("Socket closed")

    def bind(self):
        self.sock.bind((self.host, self.port))

    def client(self):
        """The send-receive loop with the client."""
        with self.connection as conn:
            while not self.disconnect:
                try:
                    conn.send(self.to_send)
                    # print("Sent: {}".format(self.to_send))

                    data: bytes = conn.recv(16384)
                    # try:
                    #     print("Received: {}".format(deserialize(data)))
                    # except EOFError:
                    #     pass
                    self.to_be_received = data

                    if not data:
                        print("Client sent nothing")
                        break
                except ConnectionAbortedError:
                    print("Client has closed the connection")
                    break
                except ConnectionResetError:
                    print("Client has probably closed the connection")
                    break
                # except ConnectionError:
                #     print("An unexpected error occurred")
                #     break

        self.hosting = False
        print("Hosting aborted")

    def send(self, data: bytes):
        self.to_send = data

    def receive(self) -> bytes:
        return self.to_be_received
