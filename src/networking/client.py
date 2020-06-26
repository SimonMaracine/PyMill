import socket
import pickle

from src.networking.message import Message
from src.log import get_logger

logger = get_logger(__name__)
logger.setLevel(10)


class Client:

    def __init__(self, id: int):
        self.id = id
        self.closed = False

        self._socket = None

    def __del__(self):
        print("Client object destroyed")

    def connect(self, ip: str, port: int):
        """
        Don't call this twice.

        """
        self._socket = socket.socket()

        try:
            self._socket.connect((ip, port))  # fail
        except socket.gaierror:  # Invalid ip address
            self._socket.close()
            raise
        except ConnectionRefusedError:  # No socket on that address or some other error
            self._socket.close()
            raise

        logger.info(f"Connected to ({ip}, {port})")

        self._socket.send(str(self.id).encode())  # fail

    def send_event(self, event: int, *args):
        message = Message(self.id, event, args)
        serialized_message = pickle.dumps(message)
        self._socket.send(serialized_message)  # fail

    def receive_event(self) -> Message:
        serialized_message = self._socket.recv(512)  # fail
        message = pickle.loads(serialized_message)  # fail

        return message

    def close(self):
        """
        Don't call this twice. self.close is for this purpose.

        """
        self._socket.shutdown(socket.SHUT_RDWR)  # Only this stops the socket from recv-ing for some reason
        self._socket.close()
        self.closed = True
