import pytest
import sys
sys.path.append('/home/user/cardazim')
from client import send_data
import socket
import struct

NUM = 4

class MockSocket:
    sent_data = []
    addr = None
    def connect(self, addr):
        MockSocket.addr = addr
    def send(self, data):
        MockSocket.sent_data.append(data)
    def recv(self, num):
        return struct.pack('I', NUM)
    def close(self):
        pass
    def getsockname(self):
        return self.addr[0], 4567
    def getpeername(self):
        return self.addr


@pytest.fixture
def mock_socket(monkeypatch):
    monkeypatch.setattr(socket, 'socket', MockSocket)


def test_send_data(mock_socket):
    send_data('avner', 'avner', 'where is avner?', 'no idea ):', '/home/user/Desktop/Matbuja.jpg')
    assert MockSocket.addr == ('10.100.102.76', 5000)    
