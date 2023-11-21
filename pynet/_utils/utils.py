import socket
from typing import Callable, Literal
import contextlib
import concurrent.futures as concurrent
import multiprocessing as mp

#! OBS: Study how to avoid broadcasting multiple times due to multithreading at server side
def broadcast(conns: list[socket.socket] = []):
    def broadcast_operation(operation: Callable):
        def wrapper():
            # TODO: Figure out why this is not working
            # with concurrent.ProcessPoolExecutor(max_workers=len(conns)) as executor:
            #     res = executor.map(operation, conns)
            #     return list(res)
            for conn in conns:
                operation(conn)
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


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip
