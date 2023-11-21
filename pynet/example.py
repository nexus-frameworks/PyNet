import time
from pynet.server import *
from pynet.client import *


class ExampleServer(SimpleServerSingleton):

    def send(self, conn: socket.socket, data: bytes):
        broadcast(self.conns)(lambda conn: conn.send(data))()

    def receive(self, conn: socket.socket) -> bytes:
        return conn.recv(1024)

class ExampleClient(ClientType):

    def input(self) -> bytes:
        self.user_input = input('>>> ').encode('utf-8')
        return self.user_input

    def send(self, data: bytes, *args, **kwargs) -> None:
        self.socket.send(data)

    def receive(self, *args, **kwargs) -> bytes:
        ret = self.socket.recv(1024)
        print(str(ret, 'utf-8'))
        return ret

    def disconnect_condition(self) -> bool:
        return self.user_input == b'exit'
