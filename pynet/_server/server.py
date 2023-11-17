import select
import socket
import threading
from abc import ABC, abstractmethod
from typing import Callable, Self
from pynet.utils import broadcast, open_socket, is_open
from pynet.p2p import Peer


class ServerType(ABC):

    def __init__(self, **kwargs) -> None: 
        self.__threads = []
        self.__conns = []
        self.__configs = kwargs

    @property
    def threads(self) -> list:
        return self.__threads
    
    @property
    def conns(self) -> list:
        return self.__conns
    
    def show_configs(self) -> dict:
        return self.__configs

    def config_server(self, **kwargs): 
        self.__configs = kwargs
        return self
    
    def reset_configs(self) -> None:
        self.__configs.clear()
    
    configs = property(show_configs, config_server, reset_configs)

    def start(self, on_loop: bool=False) -> None:
        i = 0
        with open_socket(*self.arguments, 'server', 
                         self.arguments.get('addr_family', socket.AF_INET), 
                         self.arguments.get('kind', socket.SOCK_STREAM)) as sock:
            self.__socket: socket.socket = sock
            self.__socket.listen(self.arguments.get('backlog', 5))
            while i != self.arguments.get('max_connections', None):
                ready, _, _ = select.select([self.__socket], [], [])
                if ready:
                    self.accept_client()
                    i += 1
                if self.disconnect_condition():
                    break
            if on_loop:
                self.loop()

    def loop(self) -> None:
        while True:
            if self.disconnect_condition():
                break

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