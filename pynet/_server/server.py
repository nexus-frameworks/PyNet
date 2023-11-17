import socket
import threading
from abc import ABC, abstractmethod
from typing import Callable, Self
from pynet._utils.utils import broadcast


class ServerType(ABC):

    conns = None
    __instances = None
    __args = None
    __kwargs = None


    def __init__(self, **kwargs) -> None: 
        self.__threads = []
        self.__arguments = kwargs

    @property
    def threads(self) -> list:
        return self.__threads
    
    @property
    def arguments(self) -> tuple:
        return self.__arguments

    def boot_server(self): ...
    def start(self): ...
    def handle_client(self, client_socket: socket.socket, addr: tuple): ...
    
    @abstractmethod
    def send(self, conn: socket.socket, data: bytes): ...
    
    @abstractmethod
    def receive(self, conn: socket.socket) -> bytes: ...
    
    @abstractmethod
    def handle_msg(self, conn: socket.socket, data: bytes): ...


class ServerSingleton(ServerType):
    def __new__(cls) -> Self:
        return super().__new__(cls)
    pass

class ServerFactory(ServerType):
    def __new__(cls) -> Self:
        return super().__new__()
    pass