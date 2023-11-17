import socket
import threading
from abc import ABC, abstractmethod
from typing import Callable, Self
from pynet.utils import broadcast, open_socket


class PeerType(ABC):
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

    def config_client(self, **kwargs):
        self.__configs = kwargs
        return self

    def reset_configs(self) -> None:
        self.__configs.clear()

    configs = property(show_configs, config_client, reset_configs)

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

