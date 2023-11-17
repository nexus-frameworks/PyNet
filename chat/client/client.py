import socket
import client.gui as gui
from typing import Callable, Self


def broadcast(conns: list[socket.socket] = []):
    def broadcast_operation(operation: Callable):
        def wrapper(*args, **kwargs):
            for conn in conns:
                operation(conn, *args, **kwargs)
        return wrapper
    return broadcast_operation


class Client:
    def __new__(cls) -> Self:
        pass

    def __init__(self) -> None:
        pass

    def boot_client(self) -> None:
        pass

    def start(self) -> None:
        pass

    def send(self, data: bytes) -> None:
        pass

    def receive(self) -> bytes:
        pass

    def handle_msg(self, data: bytes) -> None:
        pass

    
def main(host: str, port: int): ...
