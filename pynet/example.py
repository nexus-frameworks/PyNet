from pynet.server import *
from pynet.client import *


class ExampleServer(ServerSingleton):

    def handle_client(self, conn: socket.socket, addr: tuple):
        print(f'Connected to {addr}')
        while True:
            data = self.receive(conn)
            if data == b'':
                break
            print(f'Received {data} from {addr}')
            self.send(conn, data)
        print(f'Disconnected from {addr}')

    def send(self, conn: socket.socket, data: bytes):
        broadcast(self.conns)(lambda conn: conn.send(data))()

    def receive(self, conn: socket.socket) -> bytes:
        return conn.recv(1024)

    def __exit__(self, *args, **kwargs):
        print('Server closed')


class ExampleClient(ClientType):

    def input(self) -> bytes:
        return input('>>> ').encode('utf-8')

    def send(self, data: bytes, *args, **kwargs) -> None:
        self.socket.send(data)

    def receive(self, *args, **kwargs) -> bytes:
        ret = self.socket.recv(1024)
        print(str(ret, 'utf-8'))
        return ret

    def disconnect_condition(self) -> bool:
        return self.input() == b'exit'
