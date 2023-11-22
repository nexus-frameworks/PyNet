import select
import socket
import threading
import inspect
from abc import ABC, abstractmethod
from typing import TypeVar
from pynet.utils import broadcast, open_socket, is_open
from pynet._base.base import Base, BaseFactory

class ServerType(Base):

    def config_server(self, **kwargs):
        self.configs = kwargs
        return self
    
    def start(self) -> 'ServerType':
        self.socket = socket.socket(self.configs.get('addr_family', socket.AF_INET), 
                         self.configs.get('kind', socket.SOCK_STREAM))
        self.socket.bind((self.configs.get('host', 'localhost'), self.configs['port']))
        return self

    def run(self) -> None:
        i = 0
        #TODO: Figure out how to make the socket close here properly
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

    def wait(self) -> None:
        [thread.join() for thread in self.threads]

    def accept_client(self) -> None:
        conn, addr = self.socket.accept()
        self.conns.append(conn)
        thread = threading.Thread(target=self.handle_client, args=(conn, addr))
        self.threads.append(thread)
        thread.start()

    @abstractmethod   
    def handle_client(self, conn: socket.socket, addr: tuple): 
        pass

    def remove_client(self, conn: socket.socket) -> None:
        self.conns.remove(conn)
        conn.close()
    
    @abstractmethod
    def send(self, conn: socket.socket, data: bytes):
        pass
    
    @abstractmethod
    def receive(self, conn: socket.socket) -> bytes:
        pass

    def disconnect_condition(self) -> bool:
        return all(not is_open(conn) for conn in self.conns)
    
    def __enter__(self) -> 'ServerType':
        return self.start()
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.socket.close()
        [conn.close() for conn in self.conns]


S = TypeVar('S', bound=ServerType)

class ServerFactory(BaseFactory):

    _baseclasses = [ServerType]
    
    def make_server_class(self, name: str, base: S = ServerType, **methods) -> S:
        ret = None
        if base not in self._baseclasses:
            raise ValueError("Invalid base class. Must be one of the following: " + ' '.join([i.__name__ for i in self._baseclasses]))
        if name not in self._classes:
            abc_methods = {key: inspect.getsource(value) for key, value in methods.items()}
            ret = type(name, (base,), abc_methods)
            self._classes.append(ret)
        else:
            ret = eval(name)
        return ret

    def make_server(self, name: str, base: S = ServerType, **methods) -> S:
        cls = self.make_server_class(name, base, **methods)
        return cls()

    __call__ = make_server


class ServerSingleton(ServerType):
    _instance = None

    def _new_(cls) -> 'ServerSingleton':
        if not cls._instance:
            cls._instance = super()._new_(cls)
        return cls._instance


class SimpleServer(ServerType):
    def handle_client(self, conn: socket, addr: tuple):
        print(f'Connected to {addr}')
        while True:
            data = self.receive(conn)
            if data == b'':
                break
            print(f'Received {data} from {addr}')
            self.send(conn, data)
        print(f'Disconnected from {addr}')
        self.remove_client(conn)


class SimpleServerSingleton(ServerSingleton, SimpleServer): ...
