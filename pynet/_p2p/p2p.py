import socket
import threading
from abc import ABC, abstractmethod
from typing import Callable, Self
from pynet.utils import broadcast, open_socket
from pynet._base.base import Base


class PeerType(Base, ABC):
    
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

