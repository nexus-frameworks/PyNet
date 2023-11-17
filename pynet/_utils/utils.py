import socket
from typing import Callable, Literal
import contextlib
import concurrent.futures as concurrent

#! OBS: Study how to avoid broadcasting multiple times due to multithreading at server side
def broadcast(conns: list[socket.socket] = []):
    def broadcast_operation(operation: Callable):
        def wrapper():
            with concurrent.ProcessPoolExecutor(max_workers=len(conns)) as executor:
                res = executor.map(operation, conns)
                return list(res)
            # for conn in conns:
            #     operation(conn, *args, **kwargs)
        return wrapper
    return broadcast_operation


@contextlib.contextmanager
def open_socket(host, port, kind: Literal['server', 'client'],*args) -> socket.socket:
    sock = socket.socket(*args)
    try:
        if kind == 'client':
            sock.connect((host, port))
        elif kind == 'server':
            sock.bind((host, port))
        else:
            raise ValueError("Invalid socket type")
        yield sock
    finally:
        sock.close()


def is_open(sock: socket.socket) -> bool:
    try:
        error_code = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        return True
    except socket.error as e:
        if e.errno == 10054:
            return False
        else:
            raise e


