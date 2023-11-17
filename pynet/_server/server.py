import socket
from typing import Callable, Self
from pynet._utils.utils import broadcast


class Server:
    conns: list[socket.socket]

    __instance: Self | None = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.conns = []
        return cls.__instance

    def __init__(self) -> None: 
        pass

    def boot_server(self): ...
    def start(self): ...
    def handle_client(self, client_socket: socket.socket, addr: tuple): ...
    def send(self, conn: socket.socket, data: bytes): ...
    def receive(self, conn: socket.socket) -> bytes: ...
    def handle_msg(self, conn: socket.socket, data: bytes): ...

