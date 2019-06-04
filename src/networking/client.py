import socket


class Client:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.server_address = (self.server_host, self.server_port)

    def run(self):
        print("Connecting to {}.\n".format(self.server_address))
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect(self.server_address)
            except ConnectionRefusedError:
                print("Couldn't connect to server {}.".format(self.server_address))
            else:
                print("Connected to server {}.".format(self.server_address))
                while True:
                    pass

    def connect(self, sock):
        try:
            sock.connect(self.server_address)
        except ConnectionRefusedError:
            print("Couldn't connect to server {}.".format(self.server_address))

    @staticmethod
    def send(sock, data):
        sock.send(data)

    @staticmethod
    def receive(sock, amount: int):
        try:
            data = sock.recv(amount)
        except ConnectionResetError as e:
            print(e)
        else:
            return data
        return None
