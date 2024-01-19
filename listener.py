import socket
from connection import Connection

class Listener:
    def __init__(self, port, host, backlog=1000):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.listening_sock = socket.socket()
        

    def __repr__(self):
        return f"Listener(port={self.port}, host='{self.host}', backlog={self.backlog})"

    def start(self):
        self.listening_sock.bind((self.host, self.port))
        self.listening_sock.listen(1)

    def accept(self):
        consock, addr = self.listening_sock.accept()
        return Connection(consock)

    def stop(self):
        self.listening_sock.close()
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *args):
        self.stop()
