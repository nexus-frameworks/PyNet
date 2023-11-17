import socket
from typing import Callable, Self



def broadcast(conns: list[socket.socket] = []): 
    def broadcast_operation(operation: Callable):
        def wrapper(*args, **kwargs):
            for conn in conns:
                operation(conn, *args, **kwargs)
        return wrapper
    return broadcast_operation 

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


def main(host: str, port: int):
    server = Server()
    server.boot_server()
    server.start()
    
if __name__ == '__main__':
    main()