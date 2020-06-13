from dataclasses import dataclass


@dataclass
class Message:
    client_id: int
    action: int
    args: tuple
