import socket


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(self.address)
            except (OSError, Exception) as e:
                print(e)
            else:
                sock.listen(3)
                print("Server started. Waiting for connection...\n")
                connection, address = sock.accept()

                with connection as conn:
                    print("Connected by client {}.".format(self.address))
                    while True:
                        pass

                print("Server closed.")

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
