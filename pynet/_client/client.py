import inspect
import socket
import threading
from abc import ABC, abstractmethod
from pynet._utils.utils import broadcast, open_socket
from typing import Callable, TypeVar
from pynet._base.base import Base, BaseFactory


class ClientType(Base):
    

    def config_client(self, **kwargs):
        self.configs = kwargs
        return self
    
    def start(self) -> 'ClientType':
        self.socket = socket.socket(self.configs.get('addr_family', socket.AF_INET),
                                    self.configs.get('kind', socket.SOCK_STREAM))
        self.socket.connect((self.configs.get('host', 'localhost'), self.configs['port']))
        return self

    def run(self) -> None:
        with open_socket(self.configs.get('host', 'localhost'), self.configs['port'], 'client', 
                         self.configs.get('addr_family', socket.AF_INET), 
                         self.configs.get('kind', socket.SOCK_STREAM)) as sock:
            self.socket: socket.socket = sock
            self.handle_connection()
            self.wait()
    
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
    def input(self) -> bytes:
        pass

    @abstractmethod
    def send(self, data: bytes, *args, **kwargs) -> None:
        pass

    def send_loop(self, *args, **kwargs) -> None:
        while True:
            data = self.input()
            self.send(data, *args, **kwargs)
            if self.disconnect_condition():
                self.disconnect()
                break
    
    @abstractmethod
    def receive(self, *args, **kwargs) -> bytes:
        pass

    def receive_loop(self, *args, **kwargs) -> None:
        while True:
            data = self.receive(*args, **kwargs)
            if self.disconnect_condition():
                self.disconnect()
                break
        
    def disconnect(self) -> None:
        self.socket.close()

    def __enter__(self) -> 'ClientType':
        return self.start()
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.socket.close()


C = TypeVar('C', bound=ClientType)

class ClientFactory(BaseFactory):

    _baseclasses = [ClientType]

    def make_client_class(self, name: str, base: C = ClientType, **methods) -> C:
        ret = None
        if base not in self._baseclasses:
            raise ValueError("Invalid base class. Must be one of the following: " +
                             ' '.join([i.__name__ for i in self._baseclasses]))
        if name not in self._classes:
            abc_methods = {key: inspect.getsource(
                value) for key, value in methods.items()}
            ret = type(name, (base,), abc_methods)
            self._classes.append(ret)
        else:
            ret = eval(name)
        return ret

    def make_client(self, name: str, base: C = ClientType, **methods) -> C:
        cls = self.make_client_class(name, base, **methods)
        return cls()

    __call__ = make_client
