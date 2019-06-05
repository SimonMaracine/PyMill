import socket
import threading


class Server:
    server_running = False

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None

    def run(self):
        if not Server.server_running:
            Server.server_running = True
            threading.Thread(target=self.listen_for_connection, daemon=True).start()

    @staticmethod
    def send(sock, data: bytes):
        sock.send(data)

    @staticmethod
    def receive(sock, amount: int) -> bytes:
        try:
            data = sock.recv(amount)
        except ConnectionResetError as e:
            print(e)
        else:
            return data
        return bytes()

    def listen_for_connection(self):
        with self.sock as sock:
            try:
                sock.bind(self.address)
            except (OSError, Exception) as e:
                print(e)
            else:
                sock.settimeout(30)
                sock.listen(3)
                print("Server started. Waiting for connection...\n")
                try:
                    connection, address = sock.accept()
                    print("Connected by client {}.".format(self.address))
                except OSError:
                    print("Server closed")
                    Server.server_running = False
                    connection = None

        self.connection = connection
