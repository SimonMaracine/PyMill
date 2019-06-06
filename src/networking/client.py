import socket


class Client:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_address = (self.server_host, self.server_port)
        self.connected_to_server = False

    def run(self) -> bool:
        print("Connecting to {}.\n".format(self.server_address))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if self.connect_to_server(sock):
                return True
            else:
                return False

    def connect_to_server(self, sock) -> bool:
        try:
            sock.connect(self.server_address)
        except ConnectionRefusedError:
            print("Couldn't connect to server {}.".format(self.server_address))
            return False
        else:
            print("Connected to server {}.".format(self.server_address))
            self.connected_to_server = True
            return True

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
