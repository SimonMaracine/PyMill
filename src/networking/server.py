import socket
import threading
import pickle
import time

from src.networking.message import Message
from src.constants import *
from src.log import get_logger

logger = get_logger(__name__)
logger.setLevel(10)


class Server:

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

        self.finished_listening = False

        self._serving_sockets = []  # This is to force closing the sockets

        self._running = True
        self._send_to_client = -1

        self._server_socket = socket.socket()  # Listening socket

        try:
            self._server_socket.bind((self.ip, self.port))  # fail
        except socket.gaierror:  # Invalid ip address
            raise
        except OSError:  # Address already in use or some other error
            raise

        self._server_socket.settimeout(30)
        self._server_socket.listen(3)

        logger.info(f"Server started on ({self.ip}, {self.port})")
        threading.Thread(target=self._listen, daemon=True).start()

        self._lock = threading.Lock()
        self._message_to_send = None

    def __del__(self):
        print("Server object destroyed")

    def _listen(self):
        for _ in range(2):
            try:
                connection, address = self._server_socket.accept()  # fail
            except socket.timeout:
                self._server_socket.close()
                raise
            except ConnectionRefusedError:  # The socket was not bound
                self._server_socket.close()
                raise

            try:
                client_id = int(connection.recv(64).decode())  # fail
            except ValueError:  # Connection sent nothing
                self._server_socket.close()
                raise
            threading.Thread(target=self._serve_client, daemon=True, args=(connection, client_id)).start()
            self._serving_sockets.append(connection)

            logger.info(f"Client {address} connected to server")

        self.finished_listening = True
        self._server_socket.close()

    def _serve_client(self, sock: socket.socket, client_id: int):
        threading.Thread(target=self._check_for_sending, daemon=True, args=(sock, client_id)).start()

        with sock:
            while self._running:
                serialized_message = sock.recv(512)  # fail
                try:
                    message = pickle.loads(serialized_message)  # fail
                except EOFError:  # serialized_message was empty
                    message = Message(client_id, CLOSE_CONNECTION, ())
                    serialized_message = pickle.dumps(message)

                with self._lock:
                    if message.client_id == 0:
                        self._send_to_client = 1
                        self._message_to_send = serialized_message
                    elif message.client_id == 1:
                        self._send_to_client = 0
                        self._message_to_send = serialized_message

    def _check_for_sending(self, sock: socket.socket, client_id: int):
        while self._running:
            with self._lock:
                if self._send_to_client == 0 and client_id == 0:
                    sock.send(self._message_to_send)  # fail
                    self._send_to_client = -1
                elif self._send_to_client == 1 and client_id == 1:
                    sock.send(self._message_to_send)  # fail
                    self._send_to_client = -1
            time.sleep(0.2)

    def close(self):
        self._running = False
        for sock in self._serving_sockets:
            try:
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
            except OSError:
                pass
        # TODO maybe close the server_socket too
