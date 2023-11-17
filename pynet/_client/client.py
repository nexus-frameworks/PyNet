import socket
from pynet._utils.utils import broadcast
from typing import Callable, Self


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

    
