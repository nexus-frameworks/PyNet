import select
import socket
import threading
from abc import ABC, abstractmethod
from typing import Callable, Self
from pynet.utils import broadcast, open_socket, is_open
from pynet._base.base import Base

class ServerType(Base, ABC):

    def config_server(self, **kwargs):
        self.configs = kwargs
        return self

    def start(self, wait_disconnect: bool=True) -> None:
        i = 0
        with open_socket(self.configs.get('host', 'localhost'), self.configs.get('port', 5432), 'server', 
                         self.configs.get('addr_family', socket.AF_INET), 
                         self.configs.get('kind', socket.SOCK_STREAM)) as sock:
            self.__socket: socket.socket = sock
            self.__socket.listen(self.configs.get('backlog', 5))
            while i != self.configs.get('max_connections', None):
                ready, _, _ = select.select([self.__socket], [], [])
                if ready:
                    self.accept_client()
                    i += 1
                if self.disconnect_condition():
                    break
            if wait_disconnect:
                self.wait()

    def wait(self) -> None:
        [thread.join() for thread in self.threads]

    def accept_client(self) -> None:
        conn, addr = self.__socket.accept()
        self.conns.append(conn)
        thread = threading.Thread(target=self.handle_client, args=(conn, addr))
        self.threads.append(thread)
        thread.start()

    @abstractmethod   
    def handle_client(self, client_socket: socket.socket, addr: tuple): 
        pass
    
    @abstractmethod
    def send(self, conn: socket.socket, data: bytes):
        pass
    
    @abstractmethod
    def receive(self, conn: socket.socket) -> bytes:
        pass

    def disconnect_condition(self) -> None:
        return all(not is_open(conn) for conn  in self.conns)
    
    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        [conn.close() for conn in self.conns]
        pass


class ServerSingleton(ServerType):
    __instance = None

    def __new__(cls) -> Self:
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

class ServerFactory(ServerType):
    def __new__(cls) -> Self:
        return super().__new__()
    pass

class ServerTest(ServerType):
    def handle_client(self, client_socket: socket, addr: tuple):
        return 
    
    def send(self, conn: socket, data: bytes):
        return 
    
    def receive(self, conn: socket) -> bytes:
        return 