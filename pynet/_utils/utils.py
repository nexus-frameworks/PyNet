import socket
from typing import Callable
import concurrent.futures

def broadcast(conns: list[socket.socket] = []):
    def broadcast_operation(operation: Callable):
        def wrapper(*args, **kwargs):
            for conn in conns:
                operation(conn, *args, **kwargs)
        return wrapper
    return broadcast_operation
