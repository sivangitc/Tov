import socket
import message

class Connection:
    def __init__(self, sock):
        self.sock = sock
        self.ip_src, self.port_src = sock.getsockname()
        self.ip_dst, self.port_dst = sock.getpeername()

    def __repr__(self):
        return f"<Connection from {self.ip_src}:{self.port_src} to {self.ip_dst}:{self.port_dst}>"
    
    def send_message(self, msg):
        self.sock.send(message.pack_msg(msg))
        print("Sending " + msg)

    def receive_message(self):
        msg = b""
        while True:
            try:
                rec = self.sock.recv(1024)
            except:
                raise Exception(f"Connection closed before finished recieving\n sock:{repr(self)}")
            if not rec:
                return message.unpack_msg(msg)
            msg += rec

    def close(self):
        self.sock.close

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return cls(sock)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
