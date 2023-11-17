import socket
import threading
from abc import ABC, abstractmethod
from pynet._utils.utils import broadcast, open_client
from typing import Callable, Self


class ClientType(ABC):

    def __init__(self) -> None:
        pass

    def boot_client(self) -> None:
        pass

    def start(self) -> None:
        pass

    @abstractmethod
    def send(self, data: bytes) -> None:
        pass
    
    @abstractmethod
    def receive(self) -> bytes:
        pass

    @abstractmethod
    def handle_msg(self, data: bytes) -> None:
        pass

    @abstractmethod
    def disconnect_condition(self) -> None:
        pass

    
