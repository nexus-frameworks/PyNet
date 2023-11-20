import socket
import threading
from abc import ABC, abstractmethod
from typing import Self


class Base(ABC):
    def __init__(self, **kwargs) -> None: 
        self.__threads = []
        self.__conns = []
        self.__configs = kwargs

    @property
    def threads(self) -> list[threading.Thread]:
        return self.__threads
    
    @property
    def conns(self) -> list[socket.socket]:
        return self.__conns
    
    def show_configs(self) -> dict:
        return self.__configs

    def reconfig(self, **kwargs): 
        self.__configs = kwargs
        return self
    
    def reset_configs(self) -> None:
        self.__configs.clear()

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def wait(self) -> None:
        pass

    @abstractmethod
    def disconnect_condition(self) -> bool:
        pass

    @abstractmethod
    def start(self) -> Self:
        pass

    @abstractmethod
    def __enter__(self) -> Self:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        pass

    configs = property(show_configs, reconfig, reset_configs)


class BaseFactory:

    _instance = None
    _classes = []
    _baseclasses = []

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
