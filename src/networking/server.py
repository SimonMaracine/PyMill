import socket
import threading
import pickle
import time

from src.log import get_logger

logger = get_logger(__name__)
logger.setLevel(10)


class Server:

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

        self.finished_listening = False

        self._send_to_client = -1

        self._server_socket = socket.socket()  # Listening socket

        self._server_socket.bind((self.ip, self.port))  # fail
        self._server_socket.settimeout(30)
        self._server_socket.listen(3)

        logger.info(f"Server started on ({self.ip}, {self.port})")
        threading.Thread(target=self._listen, daemon=True).start()

        self._lock = threading.Lock()
        self._message_to_send = None

    def _listen(self):
        for _ in range(2):
            connection, address = self._server_socket.accept()  # fail

            client_id = int(connection.recv(64).decode())  # fail
            threading.Thread(target=self._serve_client, daemon=True, args=(connection, client_id)).start()

            logger.info(f"Client {address} connected to server")

        self.finished_listening = True

    def _serve_client(self, sock: socket.socket, client_id: int):
        threading.Thread(target=self._check_for_sending, daemon=True, args=(sock, client_id)).start()

        with sock:
            while True:
                serialized_message = sock.recv(512)  # fail
                message = pickle.loads(serialized_message)  # fail

                with self._lock:
                    if message.client_id == 0:
                        self._send_to_client = 1
                        self._message_to_send = serialized_message
                    elif message.client_id == 1:
                        self._send_to_client = 0
                        self._message_to_send = serialized_message

    def _check_for_sending(self, sock: socket.socket, client_id: int):
        while True:
            with self._lock:
                if self._send_to_client == 0 and client_id == 0:
                    sock.send(self._message_to_send)  # fail
                    self._send_to_client = -1
                elif self._send_to_client == 1 and client_id == 1:
                    sock.send(self._message_to_send)  # fail
                    self._send_to_client = -1
            time.sleep(0.2)
