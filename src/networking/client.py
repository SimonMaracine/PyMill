import socket
import pickle

from src.networking.message import Message
from src.log import get_logger

logger = get_logger(__name__)
logger.setLevel(10)


class Client:

    def __init__(self, id: int):
        self.socket = None
        self.id = id
        self._connected = False

    def __del__(self):
        print("Socket destroyed")

    def connect(self, ip: str, port: int):
        if not self._connected:
            self.socket = socket.socket()

            self.socket.connect((ip, port))  # fail

            logger.info(f"Connected to ({ip}, {port})")

            self._connected = True

            self.socket.send(str(self.id).encode())  # fail

    def send_event(self, event: int, *args):
        message = Message(self.id, event, args)
        serialized_message = pickle.dumps(message)
        self.socket.send(serialized_message)  # fail

    def receive_event(self) -> Message:
        serialized_message = self.socket.recv(512)  # fail
        message = pickle.loads(serialized_message)  # fail

        return message
