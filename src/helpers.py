import socket
import threading
import pickle


class Boolean:
    def __init__(self, value: bool):
        self._value = value

    def __repr__(self) -> str:
        return "{}".format(self._value)

    def set(self, value: bool):
        self._value = value

    def get(self) -> bool:
        return self._value


def create_socket() -> socket.SocketType:
    return socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)


def create_thread(target, args=(), daemon=True) -> threading.Thread:
    return threading.Thread(target=target, args=args, daemon=daemon)


def serialize(obj) -> bytes:
    return pickle.dumps(obj)


def deserialize(obj):
    return pickle.loads(obj)


def str_to_tuple(string: str) -> tuple:
    elements = string[1:-1].split(", ")
    t = []
    for i in elements:
        i = int(i)
        t.append(i)
    return tuple(t)
