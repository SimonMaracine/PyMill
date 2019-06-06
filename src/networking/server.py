import socket
import threading


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.sock = None
        self.connection = None
        self.hosting = False
        self.waiting_for_conn = False
        self.thread = None

    def run(self):
        if not self.hosting:
            self.sock = self._create_new_socket()
            self.thread = self._create_thread()
            self.thread.start()
            self.hosting = True
            self.waiting_for_conn = True
        else:
            print("Already hosting.")

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

    def _listen_for_connection(self):
        connection = None
        with self.sock as sock:
            try:
                sock.bind(self.address)
            except (OSError, Exception) as e:
                print(e)
            else:
                sock.settimeout(5)
                sock.listen(3)
                print("Server started. Waiting for connection...\n")
                try:
                    connection, address = sock.accept()
                    print("Connected by client {}.".format(self.address))
                except OSError:
                    print("Server closed.")

        self.connection = connection
        self.waiting_for_conn = False
        if self.connection is None:
            self.hosting = False
            print("Hosting stopped.")

    def _create_thread(self) -> threading.Thread:
        if self.thread and self.thread.is_alive():
            raise RuntimeError("Current thread is alive.")
        return threading.Thread(target=self._listen_for_connection, daemon=True)

    @staticmethod
    def _create_new_socket() -> socket.SocketIO:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
