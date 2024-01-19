import argparse
import sys
import socket
import struct
import threading

def run_server(server_ip, server_port):
    """
    open server socket and start accepting client requests
    """
    sock = socket.socket()
    sock.bind((server_ip, server_port))
    sock.listen(1)

    lock = threading.Lock()

    while (True):
        consock, addr = sock.accept()
        t = threading.Thread(target=handle_client, args=(consock, addr, lock))
        t.start()


def handle_client(consock, addr, lock):
    """
    recieve and print message from client
    """
    lock.acquire()
    packed = "".encode()
    while True:
        newd = consock.recv(1024)
        if not newd:
            break
        packed += newd


    data = unpack_msg(packed)
    print("Recieved data: " + data)
    consock.close()
    lock.release()


def unpack_msg(packed):
    """
    parse byted message in format <length,msg>
    """
    (slen,) = struct.unpack("I", packed[:4])
    (msg,) = struct.unpack("%ds" % slen, packed[4:])
    msg = msg.decode()
    return msg


def get_args():
    parser = argparse.ArgumentParser(description='Start server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and getting data from client.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
