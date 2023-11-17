import socket
import threading
from abc import ABC, abstractmethod
from pynet._utils.utils import broadcast, open_socket
from typing import Callable, Self
from pynet._base.base import Base


class ClientType(Base, ABC):

    
    def config_client(self, **kwargs):
        self.configs = kwargs
        return self

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

    
# class ClientFactory(ClientType):
#     def __new__(cls) -> Self:
#         return super().__new__()