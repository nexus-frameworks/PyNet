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
        with open_socket(self.configs.get('host', 'localhost'), self.configs.get('port', 5432), 'client', 
                         self.configs.get('addr_family', socket.AF_INET), 
                         self.configs.get('kind', socket.SOCK_STREAM)) as sock:
            self.__socket: socket.socket = sock
            self.handle_connection()
            self.wait()
        pass

    def handle_connection(self) -> None:
        receive_thread = threading.Thread(target=self.receive_loop)
        send_thread = threading.Thread(target=self.send_loop)
        
        self.threads.append(receive_thread)
        self.threads.append(send_thread)

        receive_thread.start()
        send_thread.start()

    def wait(self) -> None:
        [thread.join() for thread in self.threads]

    @abstractmethod
    def send(self, data: bytes, *args, **kwargs) -> None:
        pass

    def send_loop(self, *args, **kwargs) -> None:
        while True:
            data = input()
            self.send(data, *args, **kwargs)
            if self.disconnect_condition():
                break
    
    @abstractmethod
    def receive(self, *args, **kwargs) -> bytes:
        pass

    def receive_loop(self, *args, **kwargs) -> None:
        while True:
            data = self.receive(*args, **kwargs)
            if self.disconnect_condition():
                break

    def disconnect_condition(self) -> None:
        pass

    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.__socket.close()
        pass
    
# class ClientFactory(ClientType):
#     def __new__(cls) -> Self:
#         return super().__new__()