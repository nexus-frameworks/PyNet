import select
import socket
import threading
from abc import ABC, abstractmethod
from typing import Callable, Self
from pynet.utils import broadcast, open_socket
from pynet._base.base import Base


class PeerType(Base, ABC):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__recv_threads = []
        self.__send_threads = []

    @property
    def recv_threads(self) -> list[threading.Thread]:
        return self.__recv_threads
    
    @property
    def send_threads(self) -> list[threading.Thread]:
        return self.__send_threads

    def config_peer(self, **kwargs):
        self.configs = kwargs
        return self

    def start(self) -> 'PeerType':
        self.socket = socket.socket(self.configs.get('addr_family', socket.AF_INET),
                                    self.configs.get('kind', socket.SOCK_STREAM))
        self.socket.bind(
            (self.configs.get('host', 'localhost'), self.configs['port']))
        return self

    def run(self) -> None:
        i=0
        with self:
            self.socket.listen(self.configs.get('backlog', 5))
            while i != self.configs.get('max_connections', None):
                ready, _, _ = select.select([self.socket], [], [])
                if ready:
                    self.accept_client()
                    i += 1
                if self.disconnect_condition():
                    break
            self.wait()

    def accept_client(self) -> None: ...
        # conn, addr = self.socket.accept()
        # self.conns.append(conn)
        # thread = threading.Thread(target=self.handle_client, args=(conn, addr))
        # self.threads.append(thread)
        # thread.start()

    def wait(self) -> None:
        [thread.join() for thread in self.threads]

    @abstractmethod
    def send(self, data: bytes) -> None:
        pass
    
    @abstractmethod
    def receive(self) -> bytes:
        pass

    @abstractmethod
    def disconnect_condition(self) -> None:
        pass

    def __enter__(self) -> Self:
        return self.start()
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.socket.close()
    

