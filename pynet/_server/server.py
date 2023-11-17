import socket
import threading
from abc import ABC, abstractmethod
from typing import Callable, Self
from pynet._utils.utils import broadcast, open_server


class ServerType(ABC):

    conns = None

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
    def send(self, conn: socket.socket, data: bytes):
        pass
    
    @abstractmethod
    def receive(self, conn: socket.socket) -> bytes:
        pass
    
    @abstractmethod
    def handle_msg(self, conn: socket.socket, data: bytes):
        pass

    @abstractmethod
    def disconnect_condition(self) -> None:
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