import socket
from typing import Callable
import contextlib
import concurrent.futures

def broadcast(conns: list[socket.socket] = []):
    def broadcast_operation(operation: Callable):
        def wrapper(*args, **kwargs):
            for conn in conns:
                operation(conn, *args, **kwargs)
        return wrapper
    return broadcast_operation


@contextlib.contextmanager
def open_server(host, port, *args) -> socket.socket:
    sock = socket.socket(*args)
    try:
        sock.bind((host, port))
        yield sock
    finally:
        sock.close()

@contextlib.contextmanager
def open_client(host, port, *args) -> socket.socket:
    sock = socket.socket(*args)
    try:
        sock.bind((host, port))
        yield sock
    finally:
        sock.close()